run with:
``` bash
./main.py > main.log && cat main.log | sort -u -o main.sort.log
```
(creates a log file and sorts the log-output for further development)

# Example
This project focuses on generating svg files representing examples for groups of [openstreetmap](http://osm.org) tags for ways.
I.e.
## Table
<table>
    <tr>
        <th style="text-align: center" >example image (reference, not svg)</th>
        <th style="text-align: center" >Way 1</th>
        <th style="text-align: center" >Way 2</th>
        <th style="text-align: center" >Way 3</th>
    </tr>
    <tr>
        <td><img src="img_result/strasse2_doppel_rad.png" height="300px"></td>
        <td><table>
            <tr><td style="text-align: right"><code>highway</code></td><td><code>road</code></td></tr>
            <tr><td style="text-align: right"><code>cycleway:right</code></td><td><code>separate</code></td></tr>
            <tr><td style="text-align: right"><code>bicycle:both</code></td><td><code>use_sidepath</code></td></tr>
            <tr><td style="text-align: right"><code>sidewalk:right</code></td><td><code>separate</code></td></tr>
            <tr><td style="text-align: right"><code>cycleway:left</code></td><td><code>no</code></td></tr>
            <tr><td style="text-align: right"><code>sidewalk:left</code></td><td><code>no</code></td></tr>
        </table></td>
        <td><table>
            <tr><td style="text-align: right"><code>highway</code></td><td><code>cycleway</code></td></tr>
            <tr><td style="text-align: right"><code>bicycle</code></td><td><code>designated</code></td></tr>
            <tr><td style="text-align: right"><code>bicycle:oneway</code></td><td><code>no</code></td></tr>
            <tr><td style="text-align: right"><code>traffic_sign</code></td><td><code>DE:237;1000-31</code></td></tr>
        </table></td>
        <td><table>
            <tr><td style="text-align: right"><code>highway</code></td><td><code>footway</code></td></tr>
            <tr><td style="text-align: right"><code>footway</code></td><td><code>sidewalk</code></td></tr>
        </table></td>
    </tr>
</table>

## from json
```json
{
    "tags": [{
            "Way 1": {
                "highway": "road",
                "cycleway:right": "separate",
                "bicycle:both": "use_sidepath",
                "sidewalk:right": "separate",
                "cycleway:left": "no",
                "sidewalk:left": "no"
            },
            "Way 2": {
                "highway": "cycleway",
                "bicycle": "designated",
                "bicycle:oneway": "no",
                "traffic_sign": "DE:237;1000-31"
            },
            "Way 3": {
                "highway": "footway",
                "footway": "sidewalk"
            }
        }
    ]
}
```

# File structure
| file / folder | short explanation |
| - | - |
| ├── [README.md](README.md) | |
| ├── [main.py](main.py) | main |
| ├── [main.log](main.log) | log |
| ├── [main.sort.log](main.sort.log) | sorted log, contains not yet recognized (programmed) tags |
| ├── [drawing.py](drawing.py) | creates svg files from tags |
| ├── [settings.py](settings.py) | generated default settings json and reads/writes settings json |
| ├── [draw_settings.json](draw_settings.json) | general settings how to draw some elements |
| ├── [tagging.py](tagging.py) | generate example / read / write [tags.json](tags.json) |
| ├── [tags.json](tags.json) | list of groups of ways tags to render |
| ├── [svg](svg) | folder with output svg files |
| ├── [svg.html](svg.html) | summary file with svg files in a table |
| ├── [generate.sh](generate.sh) | old script that generated images, which are now used as a reference |
| ├── [tagging.html](tagging.html) | old image summary, now reference |
| ├── [tagging.md](tagging.md) | old reference markdown file, now reference, same content as [tagging.html](tagging.html) |
| ├── [img_intermediate](img_intermediate) | |
| ├── [img_result](img_result) | old images which are now used as reference |
| ├── [img_src](img_src) | old image source which were used by [generate.sh](generate.sh) |
