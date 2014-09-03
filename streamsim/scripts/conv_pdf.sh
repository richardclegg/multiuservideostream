#!/bin/sh
input=$1
output=${input%pdf}png
echo "Converting" $input "to" $output
convert -density 200x200 -resize 100% $input $output
