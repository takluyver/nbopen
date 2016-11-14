#!/bin/bash
set -e

echo "generating .icns file for mac app..."
echo "NOTE: this will produce one warning message, because there is no"
echo "      1024x1024 icon that could be used to for the 'retina' 512x512 icon"

iconsetdir=nbopen.iconset
mkdir -p ${iconsetdir}
for size in 16 32 128 256 512; do
    s2x=$((size*2))
    cp nbopen/icons/ipynb_icon_${size}x${size}.png ${iconsetdir}/icon_${size}x${size}.png
    cp nbopen/icons/ipynb_icon_${s2x}x${s2x}.png ${iconsetdir}/icon_${size}x${size}@2x.png
done
iconutil -c icns ${iconsetdir}
rm -r ${iconsetdir}
