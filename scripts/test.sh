#/bin/bash

rm -rf "build"
rm -rf "dist"
rm -rf "nonogram.egg-info"
rm -rf "~/.local/lib/python2.7/site-packages/nonogram-1.0.0-py2.7.egg"
reset
python setup.py install --user
