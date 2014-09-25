#!/bin/bash
set -e

python3 setup.py install --user

# This sets XDG_DATA_HOME if it's not already set
echo "Installing data files to: ${XDG_DATA_HOME:=$HOME/.local/share}"

#export XDG_UTILS_DEBUG_LEVEL=1  #DEBUG

xdg-mime install application-x-ipynb+json.xml

for s in 16 24 32 48 64 128 256 512; do
    xdg-icon-resource install --noupdate --size $s --context apps "icons/ipynb_icon_${s}x${s}.png" application-x-ipynb+json
done
xdg-icon-resource forceupdate

cp nbopen.desktop "$XDG_DATA_HOME/applications/"
update-desktop-database "$XDG_DATA_HOME/applications/"

