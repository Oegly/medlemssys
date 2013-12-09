# -*- coding: utf-8 -*-
# vim: ts=4 sts=4 expandtab ai
from django.contrib import admin

from .models import Membership, MembershipType

class MembershipAdmin(admin.ModelAdmin):
    list_display = ('member', 'type', 'start', 'end',)
    raw_id_fields = ('member', )
admin.site.register(Membership, MembershipAdmin)

class MembershipTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'default_price', 'num_memberships')
admin.site.register(MembershipType, MembershipTypeAdmin)
