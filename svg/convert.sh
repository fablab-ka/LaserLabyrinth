#!/bin/bash

for f in *.svg
do
filename=$(basename "$f")
filename="${filename%.*}"
inkscape $filename.svg -w 640 -e  ~/Documents/Dropbox/WIP/pngs/$filename.png
done
