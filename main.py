#!/usr/bin/env python3
from settings import set_default_settings,get_draw_settings, write_draw_settings
from tagging import get_tags, get_example_tags
import drawing
import json
import typing

def main():
    # read draw settings,
    draw_settings = get_draw_settings()

    # generate default draw settings,
    # add default draw settings,
    set_default_settings(draw_settings)

    # save draw settings
    write_draw_settings(draw_settings)

    # generate example tags, print pretty
    tags_dict = get_example_tags()
    #print(json.dumps(tags_dict, sort_keys = True, indent = 4))

    # save example tags to file
    # with open("tags.json", "w") as outfile:
    #     json.dump(tags_dict, outfile, sort_keys=False, indent=4)


    # get tags to process from file
    tags_dict : typing.Dict = get_tags()
    tags_group : typing.List = tags_dict["tags"]

    html = "<table border=1 frame=void>\n"
    html += """    <tr>
        <th>svg</th>
        <th>Way A</th>
        <th>Way B</th>
        <th>Way C</th>
    </tr>"""

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

        html += d_file.get_HTML()
    html += "</table>\n"

    with open("tagging_generated.html", "w") as outfile:
        outfile.write(html)



if __name__ == "__main__":
    main()

