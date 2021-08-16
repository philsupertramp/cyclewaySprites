from settings import DrawSettings
import typing
from way_element import WayElement
from pprint import pprint

class Way:
    size: typing.Tuple[int, int]
    offset: typing.Tuple[int, int]
    name: str
    count: int
    total: int
    elems: typing.List[WayElement]
    tags: typing.List

    recognized_tags = {"highway":             {"road", "footway", "cycleway", "path"},
                       "lanes":               {"1", "2", "3", "4"},
                       "cycleway:right":      {"lane"},
                       "cycleway:right:lane": {"exclusive", "advisory"},
                       "divider":             {"dashed_line", "solid_line", "no"},
                       "segregated":          {"yes", "no"},
                       "separation:left":     {"grass_verge"},
                       "separation:right":    {"grass_verge"}
                       }

    # ignored tags have no renderable equivalent, thus ignore to suppress warnings
    ignored_tags = {
                    "bicycle":                     {"use_sidepath", "optional_sidepath"},
                    "bicycle:oneway":              {},
                    "bicycle:both":                {"use_sidepath", "optional_sidepath"},
                    "bicycle:left":                {"use_sidepath", "optional_sidepath"},
                    "bicycle:right":               {"use_sidepath", "optional_sidepath"},
                    "cycleway:both":               {"no", "separate"},
                    "cycleway:left":               {"no", "separate"},
                    "cycleway:right":              {"no", "separate"},
                    "cycleway:right:lane:bicycle": {},
                    "foot":                        {},
                    "footway":                     {"sidewalk"},
                    "sidewalk:both":               {"no", "separate"},
                    "sidewalk:left":               {"no", "separate"},
                    "sidewalk:right":              {"no", "separate"},
                }


    def __init__(self: 'Way', name, tags, count: int, total: int) -> 'Way':
        self.elems = []
        self.name  = name
        self.tags = tags
        self.count = count
        self.total = total

        self.filter_tags()

        #print('generating elements for way "' + self.name + '" which has', len(self.tags), "tags")
        if "highway" in self.tags:
            if self.tags["highway"] in self.recognized_tags["highway"]:
                self.add_grass_verge_left()
                if   self.tags["highway"] == "road":
                    self.create_elements_highway_road()
                elif self.tags["highway"] == "footway":
                    self.create_elements_highway_footway()
                elif self.tags["highway"] == "cycleway":
                    self.create_elements_highway_cycleway()
                elif self.tags["highway"] == "path":
                    self.create_elements_highway_path()
                self.add_grass_verge_right()
            else: # unknown highway value
                print('warning: unrecognized tag "highway"=' + '"' + self.tags["highway"] + '"', "found!")
                #pprint(self.tags, indent=5, compact=False, sort_dicts=False, width=1)
        else: # no highway tag
            print("no highway tag found!")
            pprint(self.tags, indent=9, compact=False, sort_dicts=False, width=1)

    # filter group of tags to just contain the recognized ones,
    # warn if non-recognized tags are contained

    def filter_tags(self: 'Way') -> None:
        self.filtered_tags = {}
        for tag, value in self.tags.items():
            if tag in self.recognized_tags:
                if value in self.recognized_tags[tag]:
                    self.filtered_tags[tag] = value
                else:
                    if tag not in self.ignored_tags:
                        print('warning: unrecognized value found for tag "'+tag+'"="'+value+'"')
                    elif value in self.ignored_tags[tag]:
                        print('warning: unrecognized value found for ignored tag "'+tag+'"="'+value+'"')
            elif tag in self.ignored_tags:
                if value not in self.ignored_tags[tag]:
                    print('warning: unrecognized value found for ignored tag "'+tag+'"="'+value+'"')
            else:
                print('warning: unrecognized tag "'+tag+'"="'+value+'"', "found!")


    def make_grass_verge_elem(self: 'Way') -> WayElement:
        return WayElement(DrawSettings()["gruenstreifen"]["breite"]["max"],
                           DrawSettings()["draw_height_meter"],
                           DrawSettings()["gruenstreifen"]["colour"])


    def add_grass_verge_left(self: 'Way') -> None:
        # add grass_verge if first way
        if (    self.count == 0
            or
                "separation:left" in self.filtered_tags
            and self.filtered_tags["separation:left"] == "grass_verge"
            ):
            self.elems.append(self.make_grass_verge_elem())


    def add_grass_verge_right(self: 'Way') -> None:
        # add grass_verge on the right, if last way
        if (    not self.count + 1 < self.total
            or
                "separation:right" in self.filtered_tags
            and self.filtered_tags["separation:right"] == "grass_verge"
            ):
            self.elems.append(self.make_grass_verge_elem())


    def create_elements_highway_road(self: 'Way') -> None:
        self.filtered_tags.setdefault("lanes", "2")
        self.filtered_tags.setdefault("divider", "dashed_line")

        # seitenlinie, beide seiten, linie, abstand zu bordstein
        lane_markings_width = DrawSettings()["strasse"]["linie"][ DrawSettings()["strasse"]["linie"]["seitenlinie"]["breite"] ] * 2 * 2
        if self.filtered_tags["divider"] != "no":
            # leitlinie, mittig
            lane_markings_width += DrawSettings()["strasse"]["linie"][ DrawSettings()["strasse"]["linie"]["leitlinie"]["breite"] ]

        # platz zwischen bordstein und seitenlinie
        bordstein_line_sep  = WayElement(DrawSettings()["strasse"]["linie"][ DrawSettings()["strasse"]["linie"]["seitenlinie"]["breite"] ]*2,
                                        DrawSettings()["draw_height_meter"],
                                        DrawSettings()["strasse"]["colour"])
        seitenlinie         = WayElement(DrawSettings()["strasse"]["linie"][ DrawSettings()["strasse"]["linie"]["seitenlinie"]["breite"] ],
                                         DrawSettings()["draw_height_meter"],
                                         DrawSettings()["strasse"]["linie"]["colour"])

        # if wanted, create leitlinie
        if self.filtered_tags["divider"] != "no":
            leitlinie          = WayElement(DrawSettings()["strasse"]["linie"][ DrawSettings()["strasse"]["linie"]["leitlinie"]["breite"] ],
                                            DrawSettings()["strasse"]["linie"]["leitlinie"]["laenge"],
                                            DrawSettings()["strasse"]["linie"]["colour"])
            if self.filtered_tags["divider"] == "dashed_line":
                leitlinie.set_distance(DrawSettings()["strasse"]["linie"]["leitlinie"]["abstand"],
                                       DrawSettings()["strasse"]["colour"])
                leitlinie._height =    DrawSettings()["strasse"]["linie"]["leitlinie"]["laenge"]
            elif self.filtered_tags["divider"] == "solid_line":
                # do not set distance
                leitlinie._height = DrawSettings()["draw_height_meter"]

        highway_lane       = WayElement(DrawSettings()["strasse"]["spurbreite"],
                                        DrawSettings()["draw_height_meter"],
                                        DrawSettings()["strasse"]["colour"])
        bordstein          = WayElement(DrawSettings()["strasse"]["bordstein"]["breite"],
                                        DrawSettings()["strasse"]["bordstein"]["laenge"],
                                        DrawSettings()["strasse"]["bordstein"]["colour"])
        bordstein.set_distance(DrawSettings()["strasse"]["bordstein"]["abstand"],
                               DrawSettings()["strasse"]["bordstein"]["background_colour"])

        self.elems.append(bordstein)
        self.elems.append(bordstein_line_sep)
        self.elems.append(seitenlinie)

        # add road lanes and lane markings
        for lane_num in range(int(self.filtered_tags["lanes"])):
            self.elems.append(highway_lane)
            if int(self.filtered_tags["lanes"]) > 1 and lane_num +1 < int(self.filtered_tags["lanes"]):
                if leitlinie:
                    self.elems.append(leitlinie)

        # cycleway = lane
        if ( "cycleway:right" in self.filtered_tags and self.filtered_tags["cycleway:right"] == "lane"):
            if ( "cycleway:right:lane" in self.filtered_tags and self.filtered_tags["cycleway:right:lane"] == "exclusive"):
                linie_links = WayElement(DrawSettings()["strasse"]["linie"][ DrawSettings()["cycleway"]["ausgeschildert"]["radfahrstreifen"]["seitenlinie"]["links"]["breite"] ],
                                         DrawSettings()["cycleway"]["ausgeschildert"]["radfahrstreifen"]["seitenlinie"]["links"]["laenge"],
                                         DrawSettings()["strasse"]["linie"]["colour"])
                linie_links.set_distance(DrawSettings()["cycleway"]["ausgeschildert"]["radfahrstreifen"]["seitenlinie"]["links"]["abstand"],
                                         DrawSettings()["strasse"]["colour"])
                self.elems.append(linie_links)

                linie_abstand = WayElement(0.05,
                                           DrawSettings()["draw_height_meter"],
                                           DrawSettings()["strasse"]["colour"])

                self.elems.append(linie_abstand)
                self.elems.append(WayElement(DrawSettings()["cycleway"]["ausgeschildert"]["radfahrstreifen"]["breite"]["min"],
                                             DrawSettings()["draw_height_meter"],
                                             DrawSettings()["cycleway"]["ausgeschildert"]["radfahrstreifen"]["colour"]))
                self.elems.append(linie_abstand)

                linie_rechts = WayElement(DrawSettings()["strasse"]["linie"][ DrawSettings()["cycleway"]["ausgeschildert"]["radfahrstreifen"]["seitenlinie"]["rechts"]["breite"] ],
                                         DrawSettings()["cycleway"]["ausgeschildert"]["radfahrstreifen"]["seitenlinie"]["rechts"]["laenge"],
                                         DrawSettings()["strasse"]["linie"]["colour"])
                linie_rechts.set_distance(DrawSettings()["cycleway"]["ausgeschildert"]["radfahrstreifen"]["seitenlinie"]["rechts"]["abstand"],
                                         DrawSettings()["strasse"]["colour"])
                self.elems.append(linie_rechts)
            elif ("cycleway:right:lane" in self.filtered_tags and self.filtered_tags["cycleway:right:lane"] == "advisory"):
                linie_links = WayElement(DrawSettings()["strasse"]["linie"][ DrawSettings()["cycleway"]["schutzstreifen"]["seitenlinie"]["links"]["breite"] ],
                                         DrawSettings()["cycleway"]["schutzstreifen"]["seitenlinie"]["links"]["laenge"],
                                         DrawSettings()["strasse"]["linie"]["colour"])
                linie_links.set_distance(DrawSettings()["cycleway"]["schutzstreifen"]["seitenlinie"]["links"]["abstand"],
                                         DrawSettings()["strasse"]["colour"])
                self.elems.append(linie_links)

                linie_abstand = WayElement(0.05,
                                           DrawSettings()["draw_height_meter"],
                                           DrawSettings()["strasse"]["colour"])

                self.elems.append(linie_abstand)
                self.elems.append(WayElement(DrawSettings()["cycleway"]["schutzstreifen"]["breite"]["min"],
                                             DrawSettings()["draw_height_meter"],
                                             DrawSettings()["strasse"]["colour"]))
                self.elems.append(linie_abstand)

                linie_rechts = WayElement(DrawSettings()["strasse"]["linie"][ DrawSettings()["cycleway"]["schutzstreifen"]["seitenlinie"]["rechts"]["breite"] ],
                                          DrawSettings()["cycleway"]["schutzstreifen"]["seitenlinie"]["rechts"]["laenge"],
                                          DrawSettings()["strasse"]["linie"]["colour"])
                linie_rechts.set_distance(DrawSettings()["cycleway"]["schutzstreifen"]["seitenlinie"]["rechts"]["abstand"],
                                          DrawSettings()["strasse"]["colour"])
                self.elems.append(linie_rechts)
            self.elems.append(bordstein_line_sep)
        else:
            self.elems.append(bordstein_line_sep)
            self.elems.append(seitenlinie)

        self.elems.append(bordstein)


    def create_elements_highway_footway(self: 'Way') -> None:
        highway_footway = WayElement(DrawSettings()["gehweg"]["breite"]["min"],
                                     DrawSettings()["draw_height_meter"],
                                     DrawSettings()["gehweg"]["colour"])
        grass_verge = self.make_grass_verge_elem()

        # TODO traffic_sign="*"
        # TODO bicycle="yes"

        self.elems.append(highway_footway)


    def create_elements_highway_cycleway(self: 'Way') -> None:
        highway_cycleway = WayElement(DrawSettings()["cycleway"]["ausgeschildert"]["hochbord"]["breite"]["opt"],
                                      DrawSettings()["draw_height_meter"],
                                      DrawSettings()["cycleway"]["colour"])
        gruenstreifen = self.make_grass_verge_elem()

        # TODO traffic_sign="*"

        self.elems.append(highway_cycleway)


    def create_elements_highway_path(self: 'Way') -> None:
        self.filtered_tags.setdefault("segregated", "no")
        if self.filtered_tags["segregated"] == "yes":
            cycleway =   WayElement(DrawSettings()["cycleway"]["hochbord"]["breite"]["min"],
                                    DrawSettings()["draw_height_meter"],
                                    DrawSettings()["cycleway"]["colour"])
            self.elems.append(cycleway)
            highway_path = WayElement(DrawSettings()["weg"]["breite"]["min"],
                                      DrawSettings()["draw_height_meter"],
                                      DrawSettings()["weg"]["colour"])
        else:
            highway_path = WayElement(DrawSettings()["weg"]["breite"]["min"],
                                      DrawSettings()["draw_height_meter"],
                                      DrawSettings()["weg"]["colour"])
        self.elems.append(highway_path)

        # TODO traffic_sign="*"


    def get_elements(self: 'Way') -> typing.Generator[WayElement, None, None]:
        for elem in self.elems:
            yield elem


    def add_rect(self: 'Way', width, height, colour = "grey"):
        self.elems.insert(WayElement(width, height, colour))
