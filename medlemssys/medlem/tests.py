# -*- coding: utf-8 -*-
# vim: ts=4 sts=4 expandtab ai
from django.test import TestCase
import datetime

from medlem.models import Medlem, Giro

def lagMedlem(alder, utmeldt=False, har_betalt=False, name=""):
    year = datetime.date.today().year
    if not name:
        name = str(alder)
        if (har_betalt):
             name += "-betalt"
        if (utmeldt):
             name += "-utmeld"

    medlem = Medlem(
        fornamn=name,
        etternamn="E",
        fodt=year - alder,
        postnr="5000")

    if (utmeldt):
        medlem.utmeldt_dato = datetime.datetime.now()

    medlem.save()

    if (har_betalt):
        g = Giro(medlem=medlem,
                 belop=80,
                 innbetalt_belop=80,
                 innbetalt=datetime.datetime.now())
        g.save()

    return medlem

def lagTestMedlemar():
    medlemar = {}
    year = datetime.date.today().year

    def opprett_og_lagra_medlem(*args, **kwargs):
        medlem = lagMedlem(*args, **kwargs)
        medlemar[medlem.fornamn] = medlem
        return medlem

    opprett_og_lagra_medlem(25, utmeldt=False, har_betalt=False)
    opprett_og_lagra_medlem(25, utmeldt=True,  har_betalt=False)
    opprett_og_lagra_medlem(25, utmeldt=False, har_betalt=True)
    opprett_og_lagra_medlem(25, utmeldt=True,  har_betalt=True)

    opprett_og_lagra_medlem(12, utmeldt=False, har_betalt=False)
    opprett_og_lagra_medlem(12, utmeldt=True,  har_betalt=False)
    opprett_og_lagra_medlem(12, utmeldt=False, har_betalt=True)
    opprett_og_lagra_medlem(12, utmeldt=True,  har_betalt=True)

    opprett_og_lagra_medlem(26, utmeldt=False, har_betalt=False)
    opprett_og_lagra_medlem(26, utmeldt=True,  har_betalt=False)
    opprett_og_lagra_medlem(26, utmeldt=False, har_betalt=True)
    opprett_og_lagra_medlem(26, utmeldt=True,  har_betalt=True)

    m = opprett_og_lagra_medlem(23, name="23-betaltifjor")
    m.innmeldt_dato = datetime.date(year - 2, 1, 1)
    Giro(medlem=m,
         belop=80,
         innbetalt_belop=80,
         gjeldande_aar=year - 1,
         oppretta=datetime.date(year - 1, 1, 1),
         innbetalt=datetime.date(year - 1, 1, 1)).save()
    m.save()

    m = opprett_og_lagra_medlem(23, name="23-betaltiforfjor")
    m.innmeldt_dato = datetime.date(year - 2, 1, 1)
    Giro(medlem=m,
         belop=80,
         innbetalt_belop=80,
         gjeldande_aar=year - 2,
         oppretta=datetime.date(year - 2, 1, 1),
         innbetalt=datetime.date(year - 2, 1, 1)).save()
    m.save()

    m = opprett_og_lagra_medlem(23, name="23-innmeldtifjor")
    m.innmeldt_dato = datetime.date(year - 1, 1, 1)
    Giro(medlem=m,
         belop=80,
         innbetalt_belop=0,
         gjeldande_aar=year - 1,
         oppretta=datetime.date(year - 1, 1, 1)).save()
    m.save()

    m = opprett_og_lagra_medlem(23, name="23-innmeldtifjor-utmeldtiaar")
    m.innmeldt_dato = datetime.date(year - 1, 1, 1)
    m.utmeldt_dato = datetime.date(year, 1, 1)
    Giro(medlem=m,
         belop=80,
         innbetalt_belop=0,
         gjeldande_aar=year - 1,
         oppretta=datetime.date(year - 1, 1, 1)).save()
    m.save()

    m = opprett_og_lagra_medlem(23, name="23-innmeldtiforfjor-utmeldtnesteaar")
    m.innmeldt_dato = datetime.date(year - 2, 1, 1)
    m.utmeldt_dato = datetime.date(year + 1, 1, 1)
    m.save()

    m = opprett_og_lagra_medlem(23, name="23-betaltifjor-utmeldtnesteaar")
    m.innmeldt_dato = datetime.date(year - 2, 1, 1)
    m.utmeldt_dato = datetime.date(year + 1, 1, 1)
    Giro(medlem=m,
         belop=80,
         innbetalt_belop=80,
         gjeldande_aar=year - 1,
         oppretta=datetime.date(year - 1, 1, 1),
         innbetalt=datetime.date(year - 1, 1, 1)).save()
    m.save()

    m = opprett_og_lagra_medlem(23, har_betalt=True, name="23-betalt-utmeldtnesteaar")
    m.utmeldt_dato = datetime.date(year + 1, 1, 2)
    m.save()

    # innmeldt og utmeldt i fjor
    # innmeldt i fjor, men utmeldt no
    # utmeldt til neste år

    return medlemar

class MedlemTest(TestCase):
    year = datetime.date.today().year

    def setUp(self):
        self.medlemar = lagTestMedlemar()

    def test_alle(self):
        """
        Sjekk at me faktisk fær alle når me spyrr om det
        """
        alle = Medlem.objects.alle().values_list('pk', flat=True)
        self.assertEqual(set([x.pk for x in self.medlemar.values()]), set(alle))

    def test_utmelde(self):
        utmelde = Medlem.objects.utmelde().values_list('fornamn', flat=True)
        self.assertEqual(set([
                "12-utmeld", "12-betalt-utmeld",
                "25-utmeld", "25-betalt-utmeld",
                "26-utmeld", "26-betalt-utmeld",
                "23-innmeldtifjor-utmeldtiaar",
            ]), set(utmelde))

    def test_ikkje_utmelde(self):
        ikkje_utmelde = Medlem.objects.ikkje_utmelde().values_list('fornamn', flat=True)
        self.assertEqual(set([
                "12", "12-betalt",
                "25", "25-betalt",
                "26", "26-betalt",
                "23-betaltifjor", "23-innmeldtifjor", "23-betaltiforfjor",
                "23-betalt-utmeldtnesteaar",
                "23-betaltifjor-utmeldtnesteaar",
                "23-innmeldtiforfjor-utmeldtnesteaar",
            ]), set(ikkje_utmelde))

    def test_betalande(self):
        betalande = Medlem.objects.betalande().values_list('fornamn', flat=True)
        self.assertEqual(set([
                "12-betalt",
                "25-betalt",
                "26-betalt",
                "23-betalt-utmeldtnesteaar",
            ]), set(betalande))

    def test_unge(self):
        unge = Medlem.objects.unge().values_list('fornamn', flat=True)
        self.assertEqual(set([
                "12", "12-betalt",
                "25", "25-betalt",
                "23-betaltifjor", "23-innmeldtifjor", "23-betaltiforfjor",
                "23-betalt-utmeldtnesteaar",
                "23-betaltifjor-utmeldtnesteaar",
                "23-innmeldtiforfjor-utmeldtnesteaar",
            ]), set(unge))

    #def test_potensielt_teljande(self):
    #    potensielt_teljande = Medlem.objects.potensielt_teljande().values_list('fornamn', flat=True)
    #    self.assertEqual(set([
    #            "12",
    #            "25",
    #        ]), set(potensielt_teljande))


    def test_teljande(self):
        teljande = Medlem.objects.teljande().values_list('fornamn', flat=True)
        self.assertEqual(set([
                "12-betalt",
                "25-betalt",
                "23-betalt-utmeldtnesteaar",
            ]), set(teljande))

    def test_interessante(self):
        interessante = Medlem.objects.interessante().values_list('fornamn', flat=True)
        self.assertEqual(set([
                "12-betalt", "12",
                "25-betalt", "25",
                "26-betalt", "26",
                "23-betaltifjor",
                "23-betalt-utmeldtnesteaar",
                "23-betaltifjor-utmeldtnesteaar",
            ]), set(interessante))

    def test_interessante_ifjor(self):
        ifjor = Medlem.objects.interessante(self.year-1).values_list('fornamn', flat=True)
        self.assertEqual(set([
                "23-betaltifjor", "23-innmeldtifjor", "23-betaltiforfjor",
                "23-betaltifjor-utmeldtnesteaar",
                "23-innmeldtifjor-utmeldtiaar",
            ]), set(ifjor))
