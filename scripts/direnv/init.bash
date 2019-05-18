#!/bin/bash -eu

ARG0=${BASH_SOURCE[0]}
FILE_PATH=$(readlink -f $ARG0)
FILE_NAME=$(basename $FILE_PATH)
FILE_DIR=$(dirname $FILE_PATH)

SCRIPTS_DIR=$(dirname $FILE_DIR)
REPO_DIR=$(dirname $SCRIPTS_DIR)


echo "[$FILE_NAME] START"

eval "$(direnv hook bash)"

pushd $REPO_DIR
direnv allow .
popd

echo "[$FILE_NAME] END"
