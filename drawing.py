#!/usr/bin/env python3

import typing
from pprint import pprint

if __name__ == "__main__":
    pass

import svgwrite

class Drawing:
    ways: typing.List = list()
    svg_obj: svgwrite.Drawing

    def __init__(self: 'Drawing', file_name: str = "default.svg") -> 'Drawing':
        self.svg_obj = svgwrite.Drawing(file_name, profile='tiny')

    recognized_tags = {"highway":       {"road"},
                    "cycleway:both": {"no"},
                    "sidewalk:both": {"no"}}

    def draw_group(self: 'Drawing', tag_group: typing.Dict[str, typing.Dict[str, str]]) -> None:
        print("call to draw_group")

        way_name: str
        tags: typing.Dict
        for way_name, tags in tag_group.items():
            self.add_way(way_name)
            print('"' + way_name + '"', "has", len(tags), "tags:")
            if "highway" in tags:
                if tags["highway"] in self.recognized_tags["highway"]:
                    for tag, value in tags.items():
                        if tag not in self.recognized_tags:
                            print('unrecognized tag "'+tag+'"="'+value+'"', "found!")
                        elif value not in self.recognized_tags[tag]:
                            print('unrecognized value found for tag "'+tag+'"="'+value+'"')
                        else:
                            print('"' + tag + '"="' + value + '"', "found!")
                else:
                    print('unrecognized tag "highway"=' + '"' + tags["highway"] + '"', "found!")
                    pprint(tags, indent=5, compact=False, sort_dicts=False, width=1)
            else:
                print("no highway tag found!")
                pprint(tags, indent=9, compact=False, sort_dicts=False, width=1)
            print()

    def add_way(self: 'Drawing', way_name: str) -> None:
        self.ways.append(way_name)

    def add_test_elems(self: 'Drawing') -> None:
        self.svg_obj.add(self.svg_obj.line((0, 0), (100, 10), stroke=svgwrite.rgb(10, 10, 16, '%')))
        self.svg_obj.add(self.svg_obj.text('Test', insert=(10, 10.2), fill='red'))
        self.svg_obj.add(self.svg_obj.rect((0,0),(10,10), fill='blue'))

    def save(self: 'Drawing') -> None:
        self.svg_obj.save()
