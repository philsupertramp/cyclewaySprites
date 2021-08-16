#!/usr/bin/env python3
# TODO: this file made my screen go dark red ^^ my IDE enforces PEP8
# due to it's size and complexity this might be an indicator to split into
# subfiles, but if you prefer scrolling over spread I can totally understand that.

import typing
from pprint import pprint
import svgwrite
from settings import get_draw_settings
from math import floor

# TODO: drop me
if __name__ == "__main__":
    pass

# TODO: this might be better placed in `settings` so we get the global object from
# the source
draw_settings = get_draw_settings()

class Drawing:
    ways: typing.List
    svg_obj: svgwrite.Drawing
    file_name: str
    file_name_counter = 0

    # TODO: change file_name to Optional[str] with default None, but that's probably just sugar
    def __init__(self: 'Drawing', file_name: str = "svg/default.svg") -> 'Drawing':
        if file_name == "svg/default.svg":
            file_name = "svg/default" + str(Drawing.file_name_counter) + ".svg"
            Drawing.file_name_counter += 1
        # TODO: it's adviced to initialize class attributes in the __init__ method
        # python doesn't enforce and even a user can change the structor of any object
        # but initializing attributes (even empty) tells the user that the attribute isn't present
        # during initialization
        self.ways = []
        self.file_name = file_name

    def add_group(self: 'Drawing', tag_group: typing.Dict[str, typing.Dict[str, str]]) -> None:
        way_name: str
        tags: typing.Dict
        count = 0
        for way_name, tags in tag_group.items():
            self.add_way(way_name, tags, count, len(tag_group.items()))
            count += 1

    def draw(self: 'Drawing'):

        width = 0

        way: Way
        for way in self.ways:
            elem: Way_Element
            for elem in way.get_elements():
                width += elem.width()

        self.svg_obj = svgwrite.Drawing(self.file_name,
                                        profile = 'full',
                                        size = (floor(width),
                                                floor(draw_settings["draw_height_meter"] * draw_settings["pixel_pro_meter"])))

        way: Way
        x_offset = 0
        for way in self.ways:
            elem: Way_Element
            for elem in way.get_elements():
                # print(elem)
                # TODO: why declaring it private if we want to use it outside of "Way_Element"
                if elem._distance is not None:
                    # draw dashed

                    y_offset = 0
                    # initially half at top
                    self.svg_obj.add(self.svg_obj.rect((x_offset, y_offset),(elem.width(), elem.height()/2), fill=elem.colour))
                    y_offset += elem.height()/2
                    while y_offset < draw_settings["draw_height_meter"] * draw_settings["pixel_pro_meter"]:
                        self.svg_obj.add(self.svg_obj.rect((x_offset, y_offset),(elem.width(), elem.distance()), fill=elem.background_colour))
                        y_offset += elem.distance()
                        self.svg_obj.add(self.svg_obj.rect((x_offset, y_offset),(elem.width(), elem.height()), fill=elem.colour))
                        y_offset += elem.height()
                else: # solid
                    self.svg_obj.add(self.svg_obj.rect((x_offset, 0),(elem.width(), elem.height()), fill=elem.colour))
                x_offset += elem.width()

    def add_way(self: 'Drawing', name: str, tags, count, total) -> None:
        self.ways.append(Way(name, tags, count, total))

    def add_test_elems(self: 'Drawing') -> None:
        self.svg_obj.add(self.svg_obj.line((0, 0), (100, 10), stroke=svgwrite.rgb(10, 10, 16, '%')))
        self.svg_obj.add(self.svg_obj.text('Test', insert=(10, 10.2), fill='red'))
        self.svg_obj.add(self.svg_obj.rect((0,0),(10,10), fill='blue'))

    def save(self: 'Drawing') -> None:
        self.svg_obj.save()

# TODO: CamelCase me
class Way_Element:
    _width: float
    _height: float
    _distance: float
    colour: str
    background_colour: str

    def __init__(self: 'Way_Element', width, height, colour = "grey"):
        self._width = width
        self._height = height
        self._distance = None
        self.colour = colour
        self.background_colour = None

    def set_distance(self : 'Way_Element', distance, background_colour: str) -> None:
        self._distance = distance
        self.background_colour = background_colour

    def __str__(self: 'Way_Element') -> str:
        return "Way_Element: " + str(self.__dict__)

    @staticmethod
    def convert_meter_to_pixel(val):
        # floor to avoid floating point inaccuracies and weird subpixel gaps in the rendered svg
        return floor(val * draw_settings["pixel_pro_meter"])

    def width(self: 'Way_Element') -> float:
        return self.convert_meter_to_pixel(self._width)

    def height(self: 'Way_Element') -> float:
        return self.convert_meter_to_pixel(self._height)

    def distance(self: 'Way_Element') -> float:
        return self.convert_meter_to_pixel(self._distance)

class Way:
    size: typing.Tuple[int, int]
    offset: typing.Tuple[int, int]
    name: str
    count: int
    total: int

    # ignored tags have no renderable equivalent, thus ignore to suppress warnings
    recognized_tags = {"highway":           {"road", "footway", "cycleway", "path"},
                       "cycleway:both":     {"no", "separate"}, # ignore
                       "cycleway:left":     {"no", "separate"}, # ignore
                       "cycleway:right":    {"no", "separate"}, # ignore
                       "bicycle:both":      {"use_sidepath", "optional_sidepath"}, # ignore
                       "bicycle:left":      {"use_sidepath", "optional_sidepath"}, # ignore
                       "bicycle:right":     {"use_sidepath", "optional_sidepath"}, # ignore
                       "bicycle":           {},
                       "bicycle:oneway":    {},
                       "foot":              {},
                       "footway":           {"sidewalk"}, # ignore
                       "segregated":        {},
                       "traffic_sign":      {},
                       "sidewalk:both":     {"no", "separate"}, # ignore
                       "sidewalk:left":     {"no", "separate"}, # ignore
                       "sidewalk:right":    {"no", "separate"}, # ignore
                       "width:carriageway": {},
                       "lanes":             {"1", "2", "3", "4"},
                       "divider":           {"dashed_line", "solid_line", "no"}}

    elems: typing.List[Way_Element]

    # filter group of tags to just contain the recognized ones,
    # warn if non-recognized tags are contained
    def filter_tags(self: 'Way') -> typing.Dict:
        filtered_tags = {}
        for tag, value in self.tags.items():
            if tag not in self.recognized_tags:
                print('    unrecognized tag "'+tag+'"="'+value+'"', "found!")
            elif value not in self.recognized_tags[tag]:
                print('    unrecognized value found for tag "'+tag+'"="'+value+'"')
            else:
                # print('"' + tag + '"="' + value + '"', "found!")
                filtered_tags[tag] = value
        return filtered_tags

    def make_gruenstreifen_elem(self: 'Way') -> Way_Element:
        return Way_Element(draw_settings["gruenstreifen"]["breite"]["max"],
                           draw_settings["draw_height_meter"],
                           draw_settings["gruenstreifen"]["colour"])

    def create_elements_highway_road(self: 'Way') -> None:
        tags = self.filter_tags()

        tags.setdefault("lanes", "2")
        tags.setdefault("divider", "dashed_line")

        # seitenlinie, beide seiten, linie, abstand zu bordstein
        lane_markings_width = draw_settings["strasse"]["linie"][ draw_settings["strasse"]["linie"]["seitenlinie"]["breite"] ] * 2 * 2
        if tags["divider"] != "no":
            # leitlinie, mittig
            lane_markings_width += draw_settings["strasse"]["linie"][ draw_settings["strasse"]["linie"]["leitlinie"]["breite"] ]

        tags.setdefault("width:carriageway", )

        # platz zwischen bordstein und seitenlinie
        bordstein_line_sep  = Way_Element(draw_settings["strasse"]["linie"][ draw_settings["strasse"]["linie"]["seitenlinie"]["breite"] ]*2,
                                            draw_settings["draw_height_meter"],
                                            "gray")
        seitenlinie        = Way_Element(draw_settings["strasse"]["linie"][ draw_settings["strasse"]["linie"]["seitenlinie"]["breite"] ],
                                            draw_settings["draw_height_meter"],
                                            draw_settings["strasse"]["linie"]["colour"])

        # if wanted, create leitlinie
        if tags["divider"] != "no":
            leitlinie          = Way_Element(draw_settings["strasse"]["linie"][ draw_settings["strasse"]["linie"]["leitlinie"]["breite"] ],
                                                draw_settings["strasse"]["linie"]["leitlinie"]["laenge"],
                                                draw_settings["strasse"]["linie"]["colour"])
            if tags["divider"] == "dashed_line":
                leitlinie.set_distance(draw_settings["strasse"]["linie"]["leitlinie"]["abstand"],
                                        draw_settings["strasse"]["colour"])
                leitlinie._height = draw_settings["strasse"]["linie"]["leitlinie"]["laenge"]
            elif tags["divider"] == "solid_line":
                # do not set distance
                leitlinie._height = draw_settings["draw_height_meter"]

        highway_lane       = Way_Element(draw_settings["strasse"]["spurbreite"],
                                         draw_settings["draw_height_meter"],
                                         draw_settings["strasse"]["colour"])
        bordstein          = Way_Element(draw_settings["strasse"]["bordstein"]["breite"],
                                         draw_settings["strasse"]["bordstein"]["laenge"],
                                         draw_settings["strasse"]["bordstein"]["colour"])
        bordstein.set_distance(draw_settings["strasse"]["bordstein"]["abstand"],
                               draw_settings["strasse"]["bordstein"]["background_colour"])
        gruenstreifen = self.make_gruenstreifen_elem()

        # add gruenstreifen if first way
        if self.count == 0:
            self.elems.append(gruenstreifen)
        self.elems.append(bordstein)
        self.elems.append(bordstein_line_sep)
        self.elems.append(seitenlinie)

        # add road lanes and lane markings
        for lane_num in range(int(tags["lanes"])):
            self.elems.append(highway_lane)
            if int(tags["lanes"]) > 1 and lane_num +1 < int(tags["lanes"]):
                if leitlinie:
                    self.elems.append(leitlinie)

        self.elems.append(seitenlinie)
        self.elems.append(bordstein_line_sep)
        self.elems.append(bordstein)

        # add gruenstreifen on the right, if last way
        if not self.count + 1 < self.total:
            self.elems.append(gruenstreifen)

    def create_elements_highway_footway(self: 'Way') -> None:
        tags = self.filter_tags()

        highway_footway = Way_Element(draw_settings["gehweg"]["breite"]["min"],
                                      draw_settings["draw_height_meter"],
                                      draw_settings["gehweg"]["colour"])
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
        tags = self.filter_tags()

        highway_cycleway = Way_Element(draw_settings["cycleway"]["ausgeschildert"]["hochbord"]["breite"]["opt"],
                                       draw_settings["draw_height_meter"],
                                       draw_settings["cycleway"]["colour"])
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
        tags = self.filter_tags()

        highway_path = Way_Element(draw_settings["gehweg"]["breite"]["min"],
                                   draw_settings["draw_height_meter"],
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

    # TODO: move me to the top of the class declaration, I'm important.
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

    def get_elements(self: 'Way') -> typing.Generator[Way_Element, None, None]:
        for elem in self.elems:
            yield elem

    def add_rect(self: 'Way', width, height, colour = "grey"):
        self.elems.insert(Way_Element(width, height, colour))
