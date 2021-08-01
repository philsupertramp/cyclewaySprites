#!/usr/bin/env bash

function tint_with_color()
{
    local original_image=${1}
    local tint_color=${2}

    convert $original_image -fill $tint_color -tint 50 ${tint_color}_$(basename $original_image)
    echo ${tint_color}_$(basename $original_image)
}

function overlay()
{
    local original_image=${1}
    local overlay_image=${2}

    convert $original_image $overlay_image -background black -gravity center -compose over -composite ${original_image%.*}_with_$(basename $overlay_image)
    echo ${original_image%.*}_with_$(basename $overlay_image)
}

function rotate180()
{
    convert $1 -rotate 180 ${1%.*}_180.png
    echo ${1%.*}_180.png
}

result=$(rotate180 img_src/arrow_right.png)
mv $result img_intermediate/$(basename $result)

result=$(overlay img_src/paving_stones.jpg img_src/arrow_right.png)
mv $result img_intermediate/$(basename $result)

result=$(overlay img_src/paving_stones.jpg img_intermediate/arrow_right_180.png)
mv $result img_intermediate/$(basename $result)

result=$(tint_with_color img_src/paving_stones.jpg red)
mv $result img_intermediate/$(basename $result)

result=$(overlay img_src/arrow_right.png img_intermediate/arrow_right_180.png)
mv $result img_intermediate/$(basename $result)

result=$(overlay img_intermediate/red_paving_stones.jpg img_intermediate/arrow_right_with_arrow_right_180.png)
mv $result img_intermediate/$(basename $result)


convert img_intermediate/paving_stones_with_arrow_right_180.png img_src/grass.jpg img_src/asphalt.jpg img_src/line.png img_src/asphalt.jpg img_src/grass.jpg img_intermediate/red_paving_stones_with_arrow_right_with_arrow_right_180.png img_src/grass.jpg img_intermediate/paving_stones_with_arrow_right.png +append road.png

#convert cycle_lane_up.png -rotate 180 cycle_lane_down.png
#convert foot_lane_up.png -rotate 180 cycle_lane_down.png