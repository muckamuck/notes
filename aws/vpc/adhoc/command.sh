#!/bin/bash

# We need to get back to the root
dtstr=`date +'%Y%m%d_%H%M%S'`
cd `dirname ${0}`
if [ -f "${1}" ]; then
    . ${1}
else
    echo "usage: ${0} <command-properties>"
    exit 1
fi

if [ -z "${profile}" ]; then
    stackility upsert \
        -v ${dtstr} \
        -g ${tags} \
        -p ${properties} \
        -t ${template} \
        -b ${bucket} \
        -n ${stack_name} \
        -r ${region}
else
    stackility upsert \
        -v ${dtstr} \
        -f ${profile} \
        -g ${tags} \
        -p ${properties} \
        -t ${template} \
        -b ${bucket} \
        -n ${stack_name} \
        -r ${region}
fi
