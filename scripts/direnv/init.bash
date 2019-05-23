#!/bin/bash -eu

ARG0=${BASH_SOURCE[0]}
FILE_PATH=$(readlink -f $ARG0)
FILE_NAME=$(basename $FILE_PATH)
FILE_DIR=$(dirname $FILE_PATH)

repo_dir=${1:-$(pwd)}

help_message() {
	echo ""
	echo "usage: $ARG0 <repo_dir>"
	echo ""
}

if [[ -z "$repo_dir" ]]; then help_message; exit; fi

echo "[$FILE_NAME] START"

eval "$(direnv hook bash)"

pushd $repo_dir
direnv allow .
popd

echo "[$FILE_NAME] END"
