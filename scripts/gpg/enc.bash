#!/usr/bin/env bash

set -e
set -u

ARG0=${BASH_SOURCE[0]}
FILE_PATH=$(readlink -f $ARG0)
FILE_NAME=$(basename $FILE_PATH)
FILE_DIR=$(dirname $FILE_PATH)
# FILE_DIR=`pwd`/../scripts/test
SCRIPTS_DIR=$FILE_DIR

errcho(){ >&2 echo "$@"; }

errcho "[$FILE_NAME] START"
$FILE_DIR/run.bash "enc"
errcho "[$FILE_NAME] END"
