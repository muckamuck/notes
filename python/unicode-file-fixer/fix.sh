#!/bin/bash

cd $(dirname ${0})
d=${1}

if [ -d "${d}" ]; then
    find ${d} -depth -type d | python dir_fixer.py
    python file_fixer.py ${d}
else
    echo "usage: ${0} <directory-to-fix>"
fi
