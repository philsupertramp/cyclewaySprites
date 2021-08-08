#!/usr/bin/env python3

import typing
from scoping import scoping
import json


if __name__ == "__main__":
    pass


def get_tags() -> typing.Dict:
    # read settings data from json
    tag_data = None
    with open("tags.json") as json_file:
        tag_data = json.load(json_file)
        #print(json.dumps(tag_data, sort_keys = True, indent = 4))
    return tag_data



def get_example_tags() -> typing.Dict:
    data = {"tags": list()}
    tags = data["tags"]

    tags.append({
        "Way 1": {
            "highway": "road",
            "cycleway:both": "no",
            "sidewalk:both": "no",
        }
    })
    tags.append({
        "Way 1": {
            "highway": "road",
            "cycleway:both": "no",
            "sidewalk:left": "no",
            "sidewalk:right": "separate",
        },
        "Way 2": {
            "highway": "footway",
            "footway": "sidewalk",
        }
    })
    tags.append({
        "Way 1": {
            "highway": "road",
            "cycleway:left": "no",
            "cycleway:right": "separate",
            "bicycle:right": "optional_sidepath",
            "sidewalk:left": "no",
            "sidewalk:right": "separate",
        },
        "Way 2": {
            "highway": "footway",
            "footway": "sidewalk",
            "foot": "designated",
            "bicycle": "yes",
            "maxspeed:bicycle": "walk",
            "traffic_sign": "DE:239;1022-10",
        }
    })
    tags.append({
        "Way 1": {
            "highway": "road",
            "cycleway:left": "no",
            "cycleway:right": "lane",
            "cycleway:right:lane": "advisory",
            "cycleway:right:lane:bicycle": "yes",
            "sidewalk:left": "no",
            "sidewalk:right": "separate",
        },
        "Way 2": {
            "highway": "footway",
            "footway": "sidewalk",
        }
    })
    tags.append({
        "Way 1": {
            "highway": "road",
            "lanes": "2",
            "cycleway:left": "no",
            "cycleway:right": "lane",
            "cycleway:right:lane": "advisory",
            "cycleway:right:lane:bicycle": "yes",
            "sidewalk:left": "no",
            "sidewalk:right": "separate",
        },
        "Way 2": {
            "highway": "footway",
            "footway": "sidewalk",
        }
    })
    tags.append({
        "Way 1": {
            "highway": "road",
            "lanes": "2",
            "cycleway:left": "no",
            "cycleway:right": "lane",
            "cycleway:right:lane": "exclusive",
            "cycleway:right:lane:bicycle": "designated",
            "sidewalk:left": "no",
            "sidewalk:right": "separate",
        },
        "Way 2": {
            "highway": "footway",
            "footway": "sidewalk",
        }
    })
    tags.append({
        "Way 1": {
            "highway": "road",
            "cycleway:left": "no",
            "sidewalk:left": "no",
            "cycleway:right": "separate",
            "bicycle:right": "use_sidepath",
            "sidewalk:right": "separate",
        },
        "Way 2": {
            "highway": "path",
            "footway": "sidewalk",
            "foot": "designated",
            "bicycle": "designated",
            "segregated": "no",
            "traffic_sign": "DE:240",
        }
    })
    tags.append({
        "Way 1": {
            "highway": "road",
            "cycleway:right": "separate",
            "bicycle:right": "optional_sidepath",
            "sidewalk:right": "separate",
            "cycleway:left": "no",
            "sidewalk:left": "no",
        },
        "Way 2": {
            "highway": "path",
            "bicycle": "yes",
            "bicycle:oneway": "yes",
            "foot": "designated",
            "footway": "sidewalk",
            "segregated": "yes",
        }
    })
    tags.append({
        "Way 1": {
            "highway": "road",
            "cycleway:right": "separate",
            "bicycle:right": "use_sidepath",
            "sidewalk:right": "separate",
            "cycleway:left": "no",
            "sidewalk:left": "no",
        },
        "Way 2": {
            "highway": "path",
            "bicycle": "designated",
            "bicycle:oneway": "yes",
            "foot": "designated",
            "footway": "sidewalk",
            "segregated": "yes",
            "traffic_sign": "DE:241-30",
        }
    })
    tags.append({
        "Way 1": {
            "highway": "road",
            "cycleway:right": "separate",
            "bicycle:right": "optional_sidepath",
            "sidewalk:right": "separate",
            "cycleway:left": "no",
            "sidewalk:left": "no",
        },
        "Way 2": {
            "highway": "cycleway",
            "bicycle": "yes",
            "bicycle:oneway": "yes",
        },
        "Way 3": {
            "highway": "footway",
            "footway": "sidewalk",
        }
    })
    tags.append({
        "Way 1": {
            "highway": "road",
            "cycleway:right": "separate",
            "bicycle:right": "use_sidepath",
            "sidewalk:right": "separate",
            "cycleway:left": "no",
            "sidewalk:left": "no",
        },
        "Way 2": {
            "highway": "cycleway",
            "bicycle": "designated",
            "bicycle:oneway": "yes",
            "traffic_sign": "DE:237",
        },
        "Way 3": {
            "highway": "footway",
            "footway": "sidewalk",
        }
    })
    tags.append({
        "Way 1": {
            "highway": "road",
            "cycleway:right": "separate",
            "bicycle:both": "use_sidepath",
            "sidewalk:right": "separate",
            "cycleway:left": "no",
            "sidewalk:left": "no",
        },
        "Way 2": {
            "highway": "cycleway",
            "bicycle": "designated",
            "bicycle:oneway": "no",
            "traffic_sign": "DE:237;1000-31",
        },
        "Way 3": {
            "highway": "footway",
            "footway": "sidewalk",
        }
    })
    tags.append({
        "Way 1": {
            "highway": "road",
            "cycleway:right": "separate",
            "bicycle:both": "use_sidepath",
            "sidewalk:right": "separate",
            "cycleway:left": "no",
            "sidewalk:left": "no",
        },
        "Way 2": {
            "highway": "path",
            "bicycle": "designated",
            "foot": "designated",
            "bicycle:oneway": "no",
            "segregated": "yes",
            "footway": "sidewalk",
            "traffic_sign": "DE:241;1000-31",
        }
    })
    tags.append({
        "Way 1": {
            "highway": "road",
            "cycleway:right": "separate",
            "bicycle:right": "optional_sidepath",
            "sidewalk:right": "separate",
            "cycleway:left": "no",
            "sidewalk:left": "no",
        },
        "Way 2": {
            "highway": "cycleway",
            "bicycle": "yes",
            "bicycle:oneway": "yes",
        },
        "Way 3": {
            "highway": "footway",
            "footway": "sidewalk",
        }
    })
    tags.append({
        "Way 1": {
            "highway": "road",
            "cycleway:right": "separate",
            "bicycle:right": "use_sidepath",
            "sidewalk:right": "separate",
            "cycleway:left": "no",
            "sidewalk:left": "no",
        },
        "Way 2": {
            "highway": "cycleway",
            "bicycle": "designated",
            "bicycle:oneway": "yes",
            "traffic_sign": "DE:237",
        },
        "Way 3": {
            "highway": "footway",
            "footway": "sidewalk",
        }
    })
    tags.append({
        "Way 1": {
            "highway": "road",
            "cycleway:right": "separate",
            "bicycle:both": "use_sidepath",
            "sidewalk:right": "separate",
            "cycleway:left": "no",
            "sidewalk:left": "no",
        },
        "Way 2": {
            "highway": "cycleway",
            "bicycle": "designated",
            "bicycle:oneway": "no",
            "traffic_sign": "DE:237;1000-31",
        },
        "Way 3": {
            "highway": "footway",
            "footway": "sidewalk",
        }
    })

    print(data)

    return data
