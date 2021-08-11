#!/usr/bin/env python3
from settings import set_default_settings,get_draw_settings, write_draw_settings
from tagging import get_tags
import drawing
import json
import typing

def main():

    draw_settings = get_draw_settings()
    set_default_settings(draw_settings)
    write_draw_settings(draw_settings)

    # tags_dict = get_example_tags()
    # print(json.dumps(tags_dict, sort_keys = True, indent = 4))

    # with open("tags.json", "w") as outfile:
    #     json.dump(tags_dict, outfile, sort_keys=False, indent=4)

    tags_dict : typing.Dict = get_tags()
    tags_group : typing.List = tags_dict["tags"]
    group: typing.Dict
    for group in tags_group:
        d_file = drawing.Drawing()
        d_file.add_group(group)
        d_file.draw()
        d_file.save()
        #break # for now, after first road only example


if __name__ == "__main__":
    main()

