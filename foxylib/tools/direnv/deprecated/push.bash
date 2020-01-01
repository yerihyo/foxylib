#!/bin/bash -eu

ARG0=${BASH_SOURCE[0]}
FILE_PATH=$(readlink -f $ARG0)
FILE_DIR=$(dirname $FILE_PATH)
FILE_NAME=$(basename $FILE_PATH)

SCRIPTS_DIR=$(dirname $FILE_DIR)

echo "[$FILE_NAME] START"

$SCRIPTS_DIR/lpass/push.bash "$@"

echo "[$FILE_NAME] END"
