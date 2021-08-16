#!/usr/bin/env python3
"""
General comments:
    - there's PEP8, and there's a reason for it. tools like pylint and flake8 help enforcing those standards
    - you tend to repeat yourself, try extracting functionality to reduce the code and simplify maintenance
    - some places make it verry hart schnell zu verstehen what's going on weil manche things are 
    called german names, some sind englisch. Either try using only one language, or assign constants to foreign
    values, like "gehweg" could be stored in a constant called pavement or whatever, you get the gist.

"""
from settings import set_default_settings,get_draw_settings, write_draw_settings
from tagging import get_tags, get_example_tags
# TODO: declutter module imports, import what you need.
import drawing
import json
import typing

def main():
    # TODO: those are static values, we could just load a file once instead of hardcoding this whole setup
    # read draw settings,
    draw_settings = get_draw_settings()

    # generate default draw settings,
    # add default draw settings,
    set_default_settings(draw_settings)

    # save draw settings
    write_draw_settings(draw_settings)

    # generate example tags, print pretty
    tags_dict = get_example_tags()
    # TODO: drop one of multiple prints. inside get_example_tags or here
    # alternatively: pprint(tags_dict, indent=4)
    print(json.dumps(tags_dict, sort_keys = True, indent = 4))

    # save example tags to file
    with open("tags.json", "w") as outfile:
        json.dump(tags_dict, outfile, sort_keys=False, indent=4)


    # get tags to process from file
    tags_dict : typing.Dict = get_tags()
    tags_group : typing.List = tags_dict["tags"]

    # draw each group of tags separately
    group: typing.Dict
    for group in tags_group:
        d_file = drawing.Drawing()

        # add tags
        d_file.add_group(group)

        # process tags
        d_file.draw()

        # save processed tags to a file (with default, indexed name)
        d_file.save()

if __name__ == "__main__":
    main()

