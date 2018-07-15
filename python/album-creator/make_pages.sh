#!/bin/bash

for d in $(find . -depth -type d)
do
    mkdir -p ../html/${d}
done
