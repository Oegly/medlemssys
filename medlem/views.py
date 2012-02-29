# vim: ts=4 sw=4 expandtab ai
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required

from models import Medlem, InnmeldingMedlemForm, Lokallag

def create_medlem(request):
    if request.method == 'POST':
        form = InnmeldingMedlemForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/takk/')
    else:
        form = InnmeldingMedlemForm()

    return render_to_response('create_medlem.html', {
        'form': form,
    })

@login_required
def ringjelister(request):
    lokallag = Lokallag.objects.all().order_by('andsvar')
    Medlem.objects.filter()

    return render_to_response('medlem/ringjeliste.html', {
        'lokallag': lokallag,
    })
