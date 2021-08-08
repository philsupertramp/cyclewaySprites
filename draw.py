#!/usr/bin/env python3

import typing

if __name__ == "__main__":
    pass

import svgwrite
# dwg = svgwrite.Drawing('test.svg', profile='tiny')
# dwg.add(dwg.line((0, 0), (100, 10), stroke=svgwrite.rgb(10, 10, 16, '%')))
# dwg.add(dwg.text('Test', insert=(10, 10.2), fill='red'))
# dwg.save()

def draw_group(tag_group: typing.Dict[str, typing.Dict[str, str]]):
    print("call to draw_group")
    way_name: str; tags: typing.Dict
    for way_name, tags in tag_group.items():
        print(way_name, " tags:", len(tags))

