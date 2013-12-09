# -*- coding: utf-8 -*-
# vim: ts=4 sts=4 expandtab ai
from django import forms
from django.db import models
from django.utils.timezone import now

from medlem.models import Medlem

class MembershipType(models.Model):
    name = models.CharField(max_length=200)
    default_price = models.IntegerField()

    def num_memberships(self):
        return self.membership_set.count()

    def __unicode__(self):
        return self.name

class Membership(models.Model):
    member = models.ForeignKey(Medlem)
    type = models.ForeignKey(MembershipType)

    start = models.DateTimeField(blank=True, default=now)
    end = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        end = '-{}'.format(self.end.year) if self.end else ''
        return '{s.member} {s.type} ({s.start.year}{end})'.format(s=self, end=end)

