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

# convert dragon_sm.gif    -resize 64x64  resize_dragon.gif


cp img_src/* img_intermediate
cd img_intermediate

# rotate180 arrow_right.png
# overlay paving_stones.jpg arrow_right.png
# overlay paving_stones.jpg arrow_right_180.png
# tint_with_color paving_stones.jpg red
# overlay arrow_right.png arrow_right_180.png
# overlay red_paving_stones.jpg arrow_right_with_arrow_right_180.png

# prepare intermediates
convert paving_stones.jpg paving_stones.png
convert asphalt.jpg asphalt.png

tint_with_color paving_stones.png red
tint_with_color asphalt.png red

convert line.png -resize 40x2000! line_breit.png
convert grass.jpg -resize 200x2000! grass2.png
convert line.png -resize 19x2000! line_schmal.png
convert asphalt.jpg -resize 480x2000! str_spur.png
convert asphalt.jpg -resize 758x2000! str_spur_doppel_ohne_schutzstreifen.png
convert asphalt.jpg -resize 19x2000! str_schmallinie.png
convert asphalt.jpg -resize 40x2000! str_breitlinie.png

# leitlinie
convert line.png -resize 19x320! leitlinie_mitte.png
convert line.png -resize 19x160! leitlinie_top.png
convert str_schmallinie.png -resize 19x640! leitlinie_luecke.png

convert leitlinie_top.png leitlinie_luecke.png leitlinie_mitte.png leitlinie_luecke.png leitlinie_mitte.png -append leitlinie.png
convert leitlinie.png -crop 19x2000 leitlinie.png


# fahrradschutzstreifen linie
convert line.png -resize 19x160! fss_linie_mitte.png
convert line.png -resize 19x80! fss_linie_top.png
convert str_schmallinie.png -resize 19x160! fss_linie_luecke.png

convert fss_linie_top.png fss_linie_luecke.png fss_linie_mitte.png fss_linie_luecke.png fss_linie_mitte.png fss_linie_luecke.png fss_linie_mitte.png fss_linie_luecke.png fss_linie_mitte.png fss_linie_luecke.png fss_linie_mitte.png fss_linie_luecke.png fss_linie_mitte.png -append fss_linie.png
convert fss_linie.png -crop 19x2000! fss_linie.png


convert bordstein.png -resize 26x2000! bordstein.png

convert paving_stones.png -resize 400x2000! gehweg_2.50.png

convert red_asphalt.png -resize 384x2000! hochbordradweg_2.4.png
#overlay hochbordradweg_2.4.png arrow_right.png

convert asphalt.png -resize 384x2000! gemein_hochbordradweg_2.5.png
#overlay gemein_hochbordradweg_2.5.png arrow_right.png

convert red_asphalt.png -resize 320x2000! hochbordradweg_2.0.png
#overlay hochbordradweg_2.0.png arrow_right.png

convert red_asphalt.png -resize 240x2000! hochbordradweg_1.5.png
#overlay hochbordradweg_1.5.png arrow_right.png

#convert red_asphalt.png -resize 240x2000! doppel_hochbordradweg_2.4.png
#overlay doppel_hochbordradweg_2.4.png arrow_right.png

convert red_asphalt.png -resize 128x2000! hochbordradweg_0.8.png
#overlay hochbordradweg_0.8.png arrow_right.png

convert asphalt.png -resize 201x2000! schutzstreifen_1.5.png
convert asphalt.png -resize 257x2000! schutzstreifen_1.85.png

# schutzstreifen
tint_with_color schutzstreifen_1.5.png red
tint_with_color schutzstreifen_1.85.png red

mv red_schutzstreifen_1.5.png radfahrstreifen_1.5.png
mv red_schutzstreifen_1.85.png radfahrstreifen_1.85.png


convert str_schmallinie.png line_schmal.png str_spur.png leitlinie.png str_spur.png line_schmal.png str_schmallinie.png +append road.png

convert grass2.png bordstein.png road.png bordstein.png grass2.png +append strasse_gras.png

# strasse, gras, hochbordradweg in eine richtung, gras, gehweg
convert strasse_gras.png hochbordradweg_2.0.png grass2.png gehweg_2.50.png grass2.png +append strasse2.png

# strasse, gras, hochbordradweg in eine richtung, gehweg
convert strasse_gras.png hochbordradweg_2.0.png gehweg_2.50.png grass2.png +append strasse2.1.png

convert strasse_gras.png hochbordradweg_1.5.png gehweg_2.50.png grass2.png +append strasse2.1.1.png

# strasse, hochbordradweg in eine richtung, gras, gehweg
convert grass2.png bordstein.png road.png bordstein.png hochbordradweg_2.0.png grass2.png gehweg_2.50.png grass2.png +append strasse2.2.png


# strasse, gras, hochbordradweg in zwei richtung, gras, gehweg
convert strasse_gras.png hochbordradweg_2.4.png grass2.png gehweg_2.50.png grass2.png +append strasse2_doppel.png

# strasse, gras, hochbordradweg in zwei richtung, gehweg
convert strasse_gras.png hochbordradweg_2.4.png gehweg_2.50.png grass2.png +append strasse2_doppel.1.png

# strasse, hochbordradweg in zwei richtung, gras, gehweg
convert grass2.png bordstein.png road.png bordstein.png hochbordradweg_2.4.png grass2.png gehweg_2.50.png grass2.png +append strasse2_doppel.2.png


# strasse mit fahrradschutzstreifen, leitlinie, gehweg
convert grass2.png bordstein.png \
    str_schmallinie.png line_schmal.png str_spur.png leitlinie.png str_spur.png \
        fss_linie.png schutzstreifen_1.5.png fss_linie.png \
    str_schmallinie.png \
    bordstein.png grass2.png gehweg_2.50.png grass2.png +append strasse3.png

# strasse mit fahrradschutzstreifen, ohne leitlinie, gehweg
convert grass2.png bordstein.png \
    str_schmallinie.png line_schmal.png str_spur_doppel_ohne_schutzstreifen.png \
        fss_linie.png schutzstreifen_1.5.png fss_linie.png \
    str_schmallinie.png \
    bordstein.png grass2.png gehweg_2.50.png grass2.png +append strasse3.1.png

# strasse mit radfahrstreifen, leitlinie, gehweg
convert grass2.png bordstein.png \
    str_schmallinie.png line_schmal.png str_spur.png leitlinie.png str_spur.png \
        line_breit.png radfahrstreifen_1.5.png line_schmal.png \
    str_schmallinie.png \
    bordstein.png grass2.png gehweg_2.50.png grass2.png +append strasse4.png

# strasse mit gehweg
convert grass2.png bordstein.png \
    str_schmallinie.png line_schmal.png str_spur.png leitlinie.png str_spur.png \
    line_schmal.png str_schmallinie.png \
    bordstein.png grass2.png gehweg_2.50.png grass2.png +append strasse5.png

# strasse mit gemeinsamem geh- und radweg
convert grass2.png bordstein.png \
    str_schmallinie.png line_schmal.png str_spur.png leitlinie.png str_spur.png \
    line_schmal.png str_schmallinie.png \
    bordstein.png grass2.png gemein_hochbordradweg_2.5.png grass2.png +append strasse6.png


mv strasse* ../img_result

# schilder zum drueber kleben
gr600mm="480x480"
gr420mm="336x336"

convert -background none VZ_237.svg -resize $gr600mm! VZ_237_600mm.png
convert -background none VZ_237.svg -resize $gr420mm! VZ_237_420mm.png

convert -background none VZ_239.svg -resize $gr600mm! VZ_239_600mm.png
convert -background none VZ_239.svg -resize $gr420mm! VZ_239_420mm.png

convert -background none VZ_240.svg -resize $gr600mm! VZ_240_600mm.png
convert -background none VZ_240.svg -resize $gr420mm! VZ_240_420mm.png

convert -background none VZ_241-30.svg -resize $gr600mm! VZ_241-30_600mm.png
convert -background none VZ_241-30.svg -resize $gr420mm! VZ_241-30_420mm.png

grRklei="336x252"
grRgros="480x360"
convert -background none VZ_1022-10.svg -resize $grRklei! VZ_1022-10_315x420mm.png
convert -background none VZ_1022-10.svg -resize $grRgros! VZ_1022-10_450x600mm.png

grRkleiM="336x185"
grRgrosM="480x264"
convert -background none VZ_1000-31.svg -resize $grRkleiM! VZ_1000-31_315x420mm.png
convert -background none VZ_1000-31.svg -resize $grRgrosM! VZ_1000-31_450x600mm.png

mv VZ*.png ../img_result
