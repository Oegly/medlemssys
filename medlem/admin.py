# vim: ts=4 sts=4 expandtab ai
from reversion.admin import VersionAdmin
from django.contrib.admin import helpers
from django.contrib import admin
from django.http import HttpResponse
from django.forms.models import model_to_dict
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext as _
from django.template.response import TemplateResponse
from medlemssys.settings import STATIC_URL
import csv
from filters import AdditiveSubtractiveFilter, TimeSinceFilter

from models import *

class GiroInline(admin.TabularInline):
    model = Giro
    extra = 1
    classes = ['left']
    fields = ['belop', 'kid', 'oppretta', 'innbetalt', 'desc']
class RolleInline(admin.TabularInline):
    model = Rolle
    extra = 1
    classes = ['left']

class MedlemAdmin(VersionAdmin):
    list_display = ('id', '__unicode__', 'lokallag', 'er_innmeldt',
                    'har_betalt', 'fodt_farga', 'status_html')
    list_display_links = ('id', '__unicode__')
    date_hierarchy = 'innmeldt_dato'
    list_filter = (
            'status',
            ('val', AdditiveSubtractiveFilter),
            ('_siste_medlemspengar', TimeSinceFilter),
            'lokallag',
            'fodt',
            'innmeldt_dato',
        )
    readonly_fields = ('_siste_medlemspengar', 'oppretta', 'oppdatert')
    save_on_top = True
    inlines = [RolleInline, GiroInline,]
    search_fields = ('fornamn', 'mellomnamn', 'etternamn', '=id',)
    filter_horizontal = ('val', 'tilskiping', 'nemnd')
    fieldsets = (
        (None, {
            'classes': ('left',),
            'fields': (
                ('fornamn', 'mellomnamn', 'etternamn', 'fodt', 'kjon'),
                ('postadr', 'postnr', 'ekstraadr'),
                ('epost', 'mobnr'),
                ('lokallag', 'status', 'innmeldt_dato'),
            )
            }),
        (u'Ikkje pakravde felt', {
            'classes': ('left', 'collapse'),
            'fields': (
                ('utmeldt_dato', '_siste_medlemspengar', 'user'),
                ('heimenr', 'gjer'),
                ('innmeldingstype', 'innmeldingsdetalj'),
                'merknad',
                ('val', 'nemnd', 'tilskiping'),
                ('oppretta', 'oppdatert'),
            )
        }),
    )
    actions = ['csv_member_list', 'pdf_member_list',]

    class Media:
        css = {
            "all": (STATIC_URL + "medlem.css",
                STATIC_URL + "css/forms.css",)
        }

    def queryset(self, request):
        # use our manager, rather than the default one
        qs = self.model.objects.alle()

        # we need this from the superclass method
        ordering = self.ordering or () # otherwise we might try to *None, which is bad ;)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def csv_member_list(self, request, queryset):
        liste = ""

        response = HttpResponse(mimetype="text/plain")

        dc = csv.writer(response)
        dc.writerow(model_to_dict(queryset[0]).keys())
        for m in queryset:
            a = model_to_dict(m).values()
            dc.writerow([unicode(s).encode("utf-8") for s in a])

        return response

    def pdf_member_list(self, request, queryset):
        # User has already written some text, make PDF
        if request.POST.get('post'):
            from cStringIO import StringIO
            from reportlab.pdfgen import canvas
            from reportlab.lib.units import cm #, mm

            response = HttpResponse(mimetype="application/pdf")
            response['Content-Disposition'] = 'filename=noko.pdf'

            buf = StringIO()

            # Create the PDF object, using the StringIO object as its "file."
            pdf = canvas.Canvas(buf)

            # Draw things on the PDF. Here's where the PDF generation happens.
            # See the ReportLab documentation for the full list of functionality.
            for m in queryset:
                pdf.setFontSize(16)
                pdf.drawString(1.5*cm, 24*cm, "%s" % request.POST.get('title'))

                pdf.setFontSize(10)
                infotekst = pdf.beginText(1.5*cm, 22*cm)
                infotekst.textOut("%s" % request.POST.get('text'))
                pdf.drawText(infotekst)

                pdf.setFontSize(10)
                tekst = pdf.beginText(1.5*cm, 6*cm)
                tekst.textLine("%s %s" % (m.fornamn, m.etternamn) )
                tekst.textLine("%s" % (m.postadr,) )
                tekst.textLine("%s" % (m.postnr,) )
                pdf.drawText(tekst)

                pdf.showPage()
                print "%s %s" % (m.fornamn, request.POST.get('title'))

            # Close the PDF object cleanly.
            pdf.save()

            # Get the value of the StringIO buffer and write it to the response.
            pdf = buf.getvalue()
            buf.close()
            response.write(pdf)
            print "Returning response!!"
            return response

        opts = self.model._meta
        app_label = opts.app_label
        if len(queryset) == 1:
            objects_name = force_unicode(opts.verbose_name)
        else:
            objects_name = force_unicode(opts.verbose_name_plural)

        title = _("PDF-info")

        context = {
            "title": title,
            "objects_name": objects_name,
            'queryset': queryset,
            "opts": opts,
            "app_label": app_label,
            'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
        }

        return TemplateResponse(request, 'admin/pdf_info.html', context,
                current_app=self.admin_site.name)


class MedlemInline(admin.TabularInline):
    model = Medlem
    extra = 3
    fields = ['fornamn', 'etternamn', 'postadr', 'postnr', 'epost', 'mobnr', 'fodt']

class LokallagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'namn', 'num_medlem', 'andsvar',
                    'fylkeslag', 'distrikt', 'lokalsats', 'aktivt')
    list_editable = ('namn', 'andsvar', 'lokalsats', 'aktivt')
    list_per_page = 200
    inlines = [MedlemInline,]
    prepopulated_fields = {"slug": ("namn",)}


class TilskipInline(admin.TabularInline):
    model = Medlem.tilskiping.through
    raw_id_fields = ['medlem']
class TilskipAdmin(admin.ModelAdmin):
    model = Tilskiping
    inlines = [TilskipInline,]


class NemndInline(admin.TabularInline):
    model = Medlem.nemnd.through
    raw_id_fields = ['medlem']
class NemndAdmin(admin.ModelAdmin):
    list_display = ('pk', 'namn', 'start', 'stopp',)
    list_editable = ('namn',)
    inlines = [NemndInline,]

class ValInline(admin.TabularInline):
    model = Medlem.val.through
    raw_id_fields = ['medlem']
class ValAdmin(admin.ModelAdmin):
    model = Val
    inlines = [ValInline,]

# XXX: Dette fungerer i Django 1.2
#class NemndmedlemskapInline(MedlemInline):
#    model = Medlem.nemnd.through
#class NemndAdmin(admin.ModelAdmin):
#    inlines = [NemndmedlemskapInline,]
#admin.site.register(Nemnd, NemndAdmin)

admin.site.register(Medlem, MedlemAdmin)
admin.site.register(Lokallag, LokallagAdmin)
admin.site.register(Tilskiping, TilskipAdmin)
admin.site.register(Nemnd, NemndAdmin)
admin.site.register(Val, ValAdmin)
admin.site.register(Rolletype)
