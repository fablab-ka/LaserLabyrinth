#!/bin/bash

for f in ../../svg/*.svg
do
echo $f
filename=$(basename "$f")
filename="${filename%.*}"
echo $filename

inkscape ../../svg/$filename.svg -D -d 300 -e  $filename.png
done
