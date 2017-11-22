#!/bin/bash

bucket=${1}
if [ -z "${bucket}" ]; then
    echo "usage: ${0} <bucket-name>"
    exit 1
fi

# We need to get back to the root
cd `dirname ${0}`
stackility upsert \
    -v 1 \
    -g tags.properties \
    -p stack.properties \
    -t template.json \
    -b ${bucket} \
    -n ECS-EXAMPLE \
    -r us-west-2
    #--dryrun
