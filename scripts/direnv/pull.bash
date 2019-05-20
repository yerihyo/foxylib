#!/bin/bash -eu

ARG0=${BASH_SOURCE[0]}
FILE_PATH=$(readlink -f $ARG0)
FILE_NAME=$(basename $FILE_PATH)
FILE_DIR=$(dirname $FILE_PATH)

SCRIPTS_DIR=$(dirname $FILE_DIR)

LPASS_DIR=$SCRIPTS_DIR/lpass

filepath_list=${1:-}
envname=${2:-}
repo_dir=${3:-}

echo "[$FILE_NAME] START (filepath_list=$filepath_list envname=$envname repo_dir=$repo_dir)"

$LPASS_DIR/pull.bash "$filepath_list"
$FILE_DIR/load.bash "$filepath_list" "$envname" "$repo_dir"

echo "[$FILE_NAME] END"
