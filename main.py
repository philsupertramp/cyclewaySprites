#!/usr/bin/env python3
from settings import set_default_settings,get_draw_settings, write_draw_settings
from tagging import get_example_tags, get_tags
from draw import draw_group
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
        draw_group(group)
        print()
        print()


if __name__ == "__main__":
    main()

