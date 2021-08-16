#!/usr/bin/env python3
# pylint: disable=line-too-long

import typing
from pprint import pprint
from math import floor
import svgwrite
from settings import DrawSettings
class Drawing:
    """ temporarily stores data to draw and can output it to svg and an html table referenceing the svg file """
    ways: typing.List
    svg_obj: svgwrite.Drawing
    file_name: str

    # static class member
    file_name_counter = 0

    def __init__(self: 'Drawing', file_name: typing.Optional[str] = "svg/default.svg") -> 'Drawing':
        if file_name == "svg/default.svg":
            file_name = "svg/default" + str(Drawing.file_name_counter) + ".svg"
            Drawing.file_name_counter += 1
        self.ways = []
        self.file_name = file_name

    def add_group(self: 'Drawing', tag_group: typing.Dict[str, typing.Dict[str, str]]) -> None:
        """ add a group of tags to draw """
        way_name: str
        tags: typing.Dict
        count = 0
        for way_name, tags in tag_group.items():
            self.add_way(way_name, tags, count, len(tag_group.items()))
            count += 1

    def draw(self: 'Drawing'):
        """ if all data to be used is set, call draw() """
        width = 0

        way: Way
        for way in self.ways:
            elem: WayElement
            for elem in way.get_elements():
                width += elem.width()

        self.svg_obj = svgwrite.Drawing(self.file_name,
                                        profile = 'full',
                                        size = (floor(width),
                                                floor(DrawSettings()["draw_height_meter"] * DrawSettings()["pixel_pro_meter"])))

        way: Way
        x_offset = 0
        for way in self.ways:
            elem: WayElement
            for elem in way.get_elements():
                # print(elem)
                if elem.get_distance() is not None:
                    # draw dashed

                    y_offset = 0
                    # initially half at top
                    self.svg_obj.add(self.svg_obj.rect((x_offset, y_offset),(elem.width(), elem.height()/2), fill=elem.colour))
                    y_offset += elem.height()/2
                    while y_offset < DrawSettings()["draw_height_meter"] * DrawSettings()["pixel_pro_meter"]:
                        self.svg_obj.add(self.svg_obj.rect((x_offset, y_offset), (elem.width(), elem.get_distance()), fill=elem.background_colour))
                        y_offset += elem.get_distance()
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

    @staticmethod
    def html_row(key, value, background_key = None, background_value = None) -> str:
        """ get html row for given tags, if background is given, style cell with color """
        res = """\n                <tr>\n                    <td style="text-align: right;"""
        if background_key is not None:
            res += "background:" + background_key + ";"
        res += """\"><code>"""
        res += key
        res += """</code></td>\n                    <td"""
        if background_value is not None:
            res += " style=\"background:" + background_value + ";\""
        res += """><code>"""
        res += value
        res += """</code></td>\n                </tr>"""
        return res

    def get_html(self: 'Drawing') -> str:
        """ return representation as HTML table row """
        res = """\n    <tr>\n        <td><img src=\""""
        res += self.file_name
        res += """\" height=\""""
        res += str(300)
        res += """px"></td>\n"""
        way: Way
        for way in self.ways:
            res += """        <td>\n            <table border=1 frame=void>"""
            for key, value in way.tags.items():
                background_key = None
                if key not in Way.recognized_tags:
                    if key in Way.ignored_tags:
                        background_key = "lightgrey"
                    else:
                        background_key = "red"
                background_value = None
                if key not in Way.recognized_tags or value not in Way.recognized_tags[key]:
                    if key in Way.ignored_tags and value in Way.ignored_tags[key]:
                        background_value = "lightgray"
                    else:
                        background_value = "yellow"
                res += Drawing.html_row(key, value, background_key, background_value)

            for key, value in way.filtered_tags.items():
                if key in way.tags:
                    continue
                background_key = "grey"
                if key not in Way.recognized_tags:
                    if key in Way.ignored_tags:
                        background_key = "darkgrey"
                    else:
                        background_key = "orange"
                background_value = "grey"
                if key not in Way.recognized_tags or value not in Way.recognized_tags[key]:
                    if key in Way.ignored_tags and value in Way.ignored_tags[key]:
                        background_value = "darkgray"
                    else:
                        background_value = "orange"
                res += Drawing.html_row(key, value, background_key, background_value)
            res +="""\n            </table>\n        </td>\n"""
        res += """    </tr>"""
        return res

class WayElement:
    _width: float
    _height: float
    _distance: float
    colour: str
    background_colour: str

    def __init__(self: 'WayElement', width, height, colour = "grey"):
        self._width = width
        self._height = height
        self._distance = None
        self.colour = colour
        self.background_colour = None

    def set_distance(self : 'WayElement', distance, background_colour: str) -> None:
        self._distance = distance
        self.background_colour = background_colour

    def __str__(self: 'WayElement') -> str:
        return "Way_Element: " + str(self.__dict__)

    def convert_meter_to_pixel(self: 'WayElement', val):
        # floor to avoid floating point inaccuracies and weird subpixel gaps in the rendered svg
        return floor(val * DrawSettings()["pixel_pro_meter"])

    def width(self: 'WayElement') -> float:
        return self.convert_meter_to_pixel(self._width)

    def height(self: 'WayElement') -> float:
        return self.convert_meter_to_pixel(self._height)

    def get_distance(self: 'WayElement') -> float:
        if self._distance is None:
            return None
        return self.convert_meter_to_pixel(self._distance)

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
        seitenlinie        = WayElement(DrawSettings()["strasse"]["linie"][ DrawSettings()["strasse"]["linie"]["seitenlinie"]["breite"] ],
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
