#!/bin/bash -eu

ARG0=${BASH_SOURCE[0]}

FILE_PATH=$(readlink -f $ARG0)
# FILE_PATH=`pwd`/color.bash
FILE_NAME=$(basename $ARG0)
FILE_DIR=$(dirname $FILE_PATH)

launchctl load $FILE_DIR/co.elastic.elasticsearch.plist
