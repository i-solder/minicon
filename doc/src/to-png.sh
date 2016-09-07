#!/bin/bash -e

soffice --headless --convert-to svg *.odg

for f in *.svg; do
  filename="${f%.*}"
  inkscape -z -e ../img/${filename}.png -d 120 $f
done

rm *.svg
