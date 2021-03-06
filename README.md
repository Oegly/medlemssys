Medlemssys
==========

Medlemsregister for norske organisasjonar.

Bygd på datamodellen til Norsk Målungdom sitt gamle Access-register. Ein del
pragmatiske løysingar som fylgje av det. Ingenting treng vera satt i stein.

INSTALLASJON
------------

    cd medlemssys

    # Lag virtuelt Python-miljø
    virtualenv env
    . env/bin/activate
    pip install -r requirements.txt

    # Set opp testdatabasa
    python medlemssys/manage.py syncdb
    python medlemssys/manage.py migrate
    python medlemssys/manage.py loaddata medlemssys/fixtures/start\_data.json

    python medlemssys/manage.py runserver


IMPORTERING AV MEDLEMSREGISTERDATA
----------------------------------

Filformatet ventar NMU-format i CSV:

Format for lag:

    DIST,FLAG,LLAG,lid,ANDSVAR,LOKALSATS

Format for medlemar:

    REGISTERKODE,LAGSNR,MEDLNR,FORNAMN,MELLOMNAMN,ETTERNAMN,
    TILSKRIFT1,TILSKRIFT2,POST,VERVA,VERV,LP,GJER,MERKNAD,
    KJØNN,INN,INNMEDL,UTB,UT_DATO,MI,MEDLEMINF,TLF_H,TLF_A,
    E_POST,H_TILSKR1,H_TILSKR2,H_POST,H_TLF,Ring_B,Post_B,
    MM_B,MNM_B,BRUKHEIME,FARRETOR,RETUR,REGBET,HEIMEADR,
    REGISTRERT,TILSKRIFT_ENDRA,FØDEÅR,Epost_B


For å importera med standardverdiar:

    # Usage: manage.py medlem_import [options] [ lokallag.csv [ medlem.csv [ betaling.csv ] ] ]
    ./manage.py medlem_import

Du kan setja standardfilene i settings/local.py. Instellingane heiter:

    MEDLEM_CSV
    GIRO_CSV
    LAG_CSV


KØYR TESTANE
------------

Det er alt for få testar, men eit par. Skriv gjerne fleire, og køyr dei ved kodeendring.

    ./manage test medlem giro statistikk
