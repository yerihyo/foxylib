#!/bin/bash -eu

ARG0=${BASH_SOURCE[0]}
FILE_PATH=$(readlink -f $ARG0)
FILE_NAME=$(basename $FILE_PATH)
FILE_DIR=$(dirname $FILE_PATH)

SCRIPTS_DIR=$(dirname $FILE_DIR)

LPASS_DIR=$SCRIPTS_DIR/lpass

env_dir=${1:-}
envname=${2:-}
repo_dir=${3:-}

echo "[$FILE_NAME] START (env_dir=$env_dir envname=$envname repo_dir=$repo_dir)"

$LPASS_DIR/pull.bash "$env_dir"
$FILE_DIR/load.bash "$env_dir" "$envname" "$repo_dir"

echo "[$FILE_NAME] END"
