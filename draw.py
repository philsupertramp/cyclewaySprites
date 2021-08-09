#!/usr/bin/env python3

import typing
from pprint import pprint

if __name__ == "__main__":
    pass

import svgwrite

# dwg = svgwrite.Drawing('test.svg', profile='tiny')
# dwg.add(dwg.line((0, 0), (100, 10), stroke=svgwrite.rgb(10, 10, 16, '%')))
# dwg.add(dwg.text('Test', insert=(10, 10.2), fill='red'))
# dwg.save()

recognized_tags = {"highway": {"footway"}, "foot": "no"}


def draw_group(tag_group: typing.Dict[str, typing.Dict[str, str]]):
    print("call to draw_group")
    way_name: str
    tags: typing.Dict
    for way_name, tags in tag_group.items():
        print('"' + way_name + '"', "has", len(tags), "tags:")
        if "highway" in tags:
            if tags["highway"] in recognized_tags["highway"]:
                for tag, value in tags.items():
                    if tag not in recognized_tags:
                        print('unrecognized tag "'+tag+'"="'+value+'"', "found!")
                    elif value not in recognized_tags[tag]:
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
