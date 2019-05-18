#!/bin/bash -eu

ARG0=${BASH_SOURCE[0]}
FILE_PATH=$(readlink -f $ARG0)
FILE_DIR=$(dirname $FILE_PATH)
FILE_NAME=$(basename $FILE_PATH)

yaml_dir=${1:-}

help_message() {
	echo ""
	echo "usage: $ARG0 <yaml_dir>"
	echo ""
}

if [[ -z "$yaml_dir" ]]; then help_message; exit; fi

echo "[$FILE_NAME] START"

lpass logout -f
$FILE_DIR/login.bash

find $yaml_dir/ -name "*.yaml" \
    | while read filepath_yaml; do

    $FILE_DIR/pull.yaml.bash "$filepath_yaml"
done

echo "[$FILE_NAME] END"
