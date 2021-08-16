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

    recognized_tags = {"highway":           {"road", "footway", "cycleway", "path"},
                       "lanes":             {"1", "2", "3", "4"},
                       "divider":           {"dashed_line", "solid_line", "no"}}

    # ignored tags have no renderable equivalent, thus ignore to suppress warnings
    ignored_tags = {"cycleway:both":     {"no", "separate"},
                    "cycleway:left":     {"no", "separate"},
                    "cycleway:right":    {"no", "separate"},
                    "bicycle":           {},
                    "foot":              {},
                    "segregated":        {},
                    "traffic_sign":      {},
                    "width:carriageway": {},
                    "bicycle:oneway":    {},
                    "bicycle:both":      {"use_sidepath", "optional_sidepath"},
                    "bicycle:left":      {"use_sidepath", "optional_sidepath"},
                    "bicycle:right":     {"use_sidepath", "optional_sidepath"},
                    "footway":           {"sidewalk"},
                    "sidewalk:both":     {"no", "separate"},
                    "sidewalk:left":     {"no", "separate"},
                    "sidewalk:right":    {"no", "separate"}}


    def __init__(self: 'Way', name, tags, count: int, total: int) -> 'Way':
        self.elems = []
        self.name  = name
        self.tags = tags
        self.count = count
        self.total = total

        #print('generating elements for way "' + self.name + '" which has', len(self.tags), "tags")
        if "highway" in self.tags:
            if   self.tags["highway"] == "road":
                self.create_elements_highway_road()
            elif self.tags["highway"] == "footway":
                self.create_elements_highway_footway()
            elif self.tags["highway"] == "cycleway":
                self.create_elements_highway_cycleway()
            elif self.tags["highway"] == "path":
                self.create_elements_highway_path()
            else: # unknown highway value
                print('    unrecognized tag "highway"=' + '"' + self.tags["highway"] + '"', "found!")
                #pprint(self.tags, indent=5, compact=False, sort_dicts=False, width=1)
        else: # no highway tag
            print("no highway tag found!")
            pprint(self.tags, indent=9, compact=False, sort_dicts=False, width=1)

    # filter group of tags to just contain the recognized ones,
    # warn if non-recognized tags are contained
    def filter_tags(self: 'Way') -> None:
        self.filtered_tags = {}
        for tag, value in self.tags.items():
            if tag not in self.recognized_tags and tag not in self.ignored_tags:
                print('    unrecognized tag "'+tag+'"="'+value+'"', "found!")
            elif ((tag in self.recognized_tags and value not in self.recognized_tags[tag])
                    or
                  (tag in self.ignored_tags and value not in self.ignored_tags[tag])):
                print('    unrecognized value found for tag "'+tag+'"="'+value+'"')
            else:
                # print('"' + tag + '"="' + value + '"', "found!")
                self.filtered_tags[tag] = value

    def make_gruenstreifen_elem(self: 'Way') -> WayElement:
        return WayElement(DrawSettings()["gruenstreifen"]["breite"]["max"],
                           DrawSettings()["draw_height_meter"],
                           DrawSettings()["gruenstreifen"]["colour"])

    def create_elements_highway_road(self: 'Way') -> None:
        self.filter_tags()

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
                                        "gray")
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
                leitlinie._height = DrawSettings()["strasse"]["linie"]["leitlinie"]["laenge"]
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
        gruenstreifen = self.make_gruenstreifen_elem()

        # add gruenstreifen if first way
        if self.count == 0:
            self.elems.append(gruenstreifen)
        self.elems.append(bordstein)
        self.elems.append(bordstein_line_sep)
        self.elems.append(seitenlinie)

        # add road lanes and lane markings
        for lane_num in range(int(self.filtered_tags["lanes"])):
            self.elems.append(highway_lane)
            if int(self.filtered_tags["lanes"]) > 1 and lane_num +1 < int(self.filtered_tags["lanes"]):
                if leitlinie:
                    self.elems.append(leitlinie)

        self.elems.append(seitenlinie)
        self.elems.append(bordstein_line_sep)
        self.elems.append(bordstein)

        # add gruenstreifen on the right, if last way
        if not self.count + 1 < self.total:
            self.elems.append(gruenstreifen)

    def create_elements_highway_footway(self: 'Way') -> None:
        self.filter_tags()

        highway_footway = WayElement(DrawSettings()["gehweg"]["breite"]["min"],
                                      DrawSettings()["draw_height_meter"],
                                      DrawSettings()["gehweg"]["colour"])
        gruenstreifen = self.make_gruenstreifen_elem()

        # add gruenstreifen if first way
        if self.count == 0:
            self.elems.append(gruenstreifen)

        # TODO traffic_sign="*"
        # TODO bicycle="yes"
        # TODO segregated="yes|no"

        self.elems.append(highway_footway)

        # add gruenstreifen on the right, if last way
        if not self.count + 1 < self.total:
            self.elems.append(gruenstreifen)

    def create_elements_highway_cycleway(self: 'Way') -> None:
        self.filter_tags()

        highway_cycleway = WayElement(DrawSettings()["cycleway"]["ausgeschildert"]["hochbord"]["breite"]["opt"],
                                       DrawSettings()["draw_height_meter"],
                                       DrawSettings()["cycleway"]["colour"])
        gruenstreifen = self.make_gruenstreifen_elem()

        # add gruenstreifen if first way
        if self.count == 0:
            self.elems.append(gruenstreifen)

        # TODO traffic_sign="*"
        # TODO segregated="yes|no"

        self.elems.append(highway_cycleway)

        # add gruenstreifen on the right, if last way
        if not self.count + 1 < self.total:
            self.elems.append(gruenstreifen)

    def create_elements_highway_path(self: 'Way') -> None:
        self.filter_tags()

        highway_path = WayElement(DrawSettings()["gehweg"]["breite"]["min"],
                                   DrawSettings()["draw_height_meter"],
                                   "#745d4c") # TODO
        gruenstreifen = self.make_gruenstreifen_elem()

        # add gruenstreifen if first way
        if self.count == 0:
            self.elems.append(gruenstreifen)

        # TODO traffic_sign="*"
        # TODO segregated="yes|no"

        self.elems.append(highway_path)

        # add gruenstreifen on the right, if last way
        if not self.count + 1 < self.total:
            self.elems.append(gruenstreifen)


    def get_elements(self: 'Way') -> typing.Generator[WayElement, None, None]:
        for elem in self.elems:
            yield elem

    def add_rect(self: 'Way', width, height, colour = "grey"):
        self.elems.insert(WayElement(width, height, colour))
