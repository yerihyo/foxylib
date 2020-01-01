#!/bin/bash -eu

ARG0=${BASH_SOURCE[0]}
FILE_PATH=$(readlink -f $ARG0)
FILE_NAME=$(basename $FILE_PATH)
FILE_DIR=$(dirname $FILE_PATH)

SCRIPTS_DIR=$(dirname $FILE_DIR)
echo "[$FILE_NAME] START"

mkdir -p $HOME/scripts
ln -s $SCRIPTS_DIR/lpass $HOME/scripts/
ln -s $SCRIPTS_DIR/direnv $HOME/scripts/

echo "[$FILE_NAME] END"
