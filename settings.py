#!/usr/bin/env python3

import typing
from scoping import scoping
import json

if __name__ == "__main__":
    pass

def get_draw_settings() -> typing.Dict:
    # read settings data from json
    settings_data = None
    with open("draw_settings.json") as json_file:
        settings_data = json.load(json_file)
        #print(json.dumps(settings_data, sort_keys = True, indent = 4))
    return settings_data

def write_draw_settings(settings_data: typing.Dict) -> None:
    with open("draw_settings.json", "w") as outfile:
        json.dump(settings_data, outfile, sort_keys=True, indent=4)

def set_default_settings(settings_data: typing.Dict) -> None:
    # set non-existent data in json

    gehweg = settings_data.setdefault("gehweg", {})
    with scoping():
        breite = gehweg.setdefault("breite", {})
        with scoping():
            breite.setdefault("old", 1.5)
            breite.setdefault("min", 2.5)

    strasse = settings_data.setdefault("strasse", {})
    with scoping():
        spurbreite = strasse.setdefault("spurbreite", 3)

        bordstein = strasse.setdefault("bordstein", {})
        with scoping():
            bordstein.setdefault("breite", 0.165)
            bordstein.setdefault("laenge", 1)
            bordstein.setdefault("abstand", 0.01)

        linie = strasse.setdefault("linie", {})
        with scoping():
            breitstrich = linie.setdefault("breitstrich", 0.25)
            schmalstrich = linie.setdefault("schmalstrich", 0.12)

            leitlinie = linie.setdefault("leitlinie", {})
            with scoping():
                # verhaeltnis laenge:luecke ist 1:2
                abstand = leitlinie.setdefault("abstand", 6)
                laenge = leitlinie.setdefault("laenge", 3) # innerorts, ist variabel
                breite = leitlinie.setdefault("breite", "schmalstrich")

            seitenlinie = linie.setdefault("seitenlinie", {}) # name ausgedacht
            with scoping():
                abstand = seitenlinie.setdefault("abstand", 0) # durchgezogen
                laenge = seitenlinie.setdefault("laenge", 1)
                breite = seitenlinie.setdefault("breite", "schmalstrich")


    cycleway = settings_data.setdefault("cycleway", {})
    with scoping():
        ausgeschildert = cycleway.setdefault("ausgeschildert", {})
        with scoping():
            hochbord = ausgeschildert.setdefault("hochbord", {})
            with scoping():
                breite = hochbord.setdefault("breite", {})
                with scoping():
                    breite.setdefault("min", 1.5)
                    breite.setdefault("opt", 2)

                # linksseitig bedeutet meist, dass dieser geteilt, also in beide richtungen benutzt werden kann/muss
                links = hochbord.setdefault("links", {})
                with scoping():
                    breite = links.setdefault("breite", {})
                    with scoping():
                        breite.setdefault("min", 2)
                        breite.setdefault("opt", 2.4)

                geh_rad = hochbord.setdefault("geh_rad", {})
                with scoping():
                    breite = geh_rad.setdefault("breite", {})
                    with scoping():
                        breite.setdefault("min", 2.5)
                        breite.setdefault("opt", "?")


            radfahrstreifen = ausgeschildert.setdefault("radfahrstreifen", {})
            with scoping():
                breite = radfahrstreifen.setdefault("breite", {})
                with scoping():
                    breite.setdefault("min", 1.6)
                    breite.setdefault("opt", "?")

                links = radfahrstreifen.setdefault("links", {})
                with scoping():
                    breite = links.setdefault("breite", {})
                    with scoping():
                        breite.setdefault("min", "?")
                        breite.setdefault("opt", "?")

        # nicht ausgeschildert, also optional
        hochbord = cycleway.setdefault("hochbord", {})
        with scoping():
            breite = hochbord.setdefault("breite", {})
            with scoping():
                breite.setdefault("min", "?")
                breite.setdefault("opt", "?")

            geh_rad = hochbord.setdefault("geh_rad", {})
            with scoping():
                breite = geh_rad.setdefault("breite", {})
                with scoping():
                    breite.setdefault("min", "?")
                    breite.setdefault("opt", "?")

        schutzstreifen = cycleway.setdefault("schutzstreifen", {})
        with scoping():
            breite = schutzstreifen.setdefault("breite", {})
            with scoping():
                breite.setdefault("min", 1.25)
                breite.setdefault("opt", 1.50)

            seitenlinie = schutzstreifen.setdefault("seitenlinie", {})
            with scoping():
                links = seitenlinie.setdefault("links", {}) # name ausgedacht
                with scoping():
                    abstand = links.setdefault("abstand", 1)
                    laenge =  links.setdefault("laenge", 1)
                    breite =  links.setdefault("breite", "schmalstrich")

                rechts = seitenlinie.setdefault("rechts", {}) # name ausgedacht
                with scoping():
                    abstand = rechts.setdefault("abstand", 0) # durchgezogen
                    laenge =  rechts.setdefault("laenge", 1)
                    breite =  rechts.setdefault("breite", "schmalstrich")

            kernfahrbahn = schutzstreifen.setdefault("kernfahrbahn", {})
            with scoping():
                breite = kernfahrbahn.setdefault("breite", {})
                with scoping():
                    breite.setdefault("min", 2.25)
                    breite.setdefault("opt", 3)

    pixel_pro_meter = settings_data.setdefault("pixel_pro_meter", 160)
    draw_height_meter = settings_data.setdefault("draw_height_meter", 10)

    schild = settings_data.setdefault("schild", {})
    with scoping():
        # um die schilder besser erkennen zu koennen im bild, stelle sie
        # nicht massstabsgetreu dar, sondern um diesen faktor vergroessert
        groessenfaktor = schild.setdefault("groessenfaktor", 5)

        rund = schild.setdefault("rund", {})
        with scoping():
            breite = schild.setdefault("breite", {}) # = durchmesser
            with scoping():
                gross = breite.setdefault("gross", 0.6)
                klein = breite.setdefault("klein", 0.42)

        zusatz = schild.setdefault("zusatz", {})
        with scoping():
            breite = zusatz.setdefault("breite", {}) # hoehe egal, da seitenverhaeltnis beizubehalten ist
            with scoping():
                gross = breite.setdefault("gross", 0.6)
                klein = breite.setdefault("klein", 0.42)

    gruenstreifen = settings_data.setdefault("gruenstreifen", {})
    with scoping():
        breite = gruenstreifen.setdefault("breite", {})
        with scoping():
            breite.setdefault("min", 0)
            breite.setdefault("max", 1.5) # quelle?

