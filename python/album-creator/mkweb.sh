#!/bin/bash

dimension=720
mkdir ../web
for big in $(find . -type f)
do
    echo "Processing: ${big}"
    d=$(dirname ${big})
    b=$(basename ${big})

    if [ ! -d "../web/${d}" ]; then
        mkdir -p  ../web/${d}
    fi

    convert ${big} -resize ${dimension}x${dimension} ../web/${d}/${b}
done
