#!/bin/bash
set -e

./osx-make-iconset.sh

python3 py2app_setup.py install
python3 py2app_setup.py py2app

INSTALL_PATH="$HOME/Applications/nbopen.app"
if [ -e $INSTALL_PATH ]; then
    rm -rf $INSTALL_PATH
fi
ln -s "$(pwd)/dist/nbopen.app" $INSTALL_PATH

