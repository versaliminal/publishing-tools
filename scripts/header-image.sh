#!/bin/bash
EXPECTED_RATIO="2.6"
ratio=$(magick identify -format "%[fx:w/h]" "${1}")
if [[ "${ratio}" != "${EXPECTED_RATIO}"* ]]; then
    echo "Ratio is out of spec: ratio=${ratio}"
fi
magick "${1}" -resize 1200 "${2}"
magick "${2}" -shave 5x5 -bordercolor "#8F3D3A" -border 5x5 "${2}"