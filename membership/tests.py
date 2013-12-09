"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

import datetime
from django.test import TestCase
from django.utils import timezone

from .models import MembershipType
from medlem.models import Medlem
from medlem.tests import lagMedlem

class MedlemTest(TestCase):

    def setUp(self):
        yesterday = timezone.now() - datetime.timedelta(days=1)
        tomorrow = timezone.now() + datetime.timedelta(days=1)
        mt = MembershipType(name='test', default_price=80)
        mt.save()
        m = lagMedlem(20, name="20-membership-yesterday-till-tomorrow")
        m.membership_set.create(type=mt, start=yesterday, end=tomorrow)
        m.save()

        m = lagMedlem(20, name="20-membership-starts-tomorrow")
        m.membership_set.create(type=mt, start=tomorrow)
        m.save()

        m = lagMedlem(20, name="20-membership-ended-yesterday")
        m.membership_set.create(type=mt, start=yesterday, end=yesterday)
        m.save()

        m = lagMedlem(20, name="20-no-membership")

    def test_valid_membership(self):
        valid = (Medlem.objects.valid_membership()
                               .values_list('fornamn', flat=True))
        self.assertEqual(set([
          "20-membership-yesterday-till-tomorrow",
        ]), set(valid))

    def test_invalid_membership(self):
        invalid = (Medlem.objects.invalid_membership()
                                 .values_list('fornamn', flat=True))
        self.assertEqual(set([
          "20-membership-starts-tomorrow",
          "20-membership-ended-yesterday",
          "20-no-membership",
        ]), set(invalid))
