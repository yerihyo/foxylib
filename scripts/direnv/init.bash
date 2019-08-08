#!/bin/bash -eu

ARG0=${BASH_SOURCE[0]}
FILE_PATH=$(readlink -f $ARG0)
FILE_NAME=$(basename $FILE_PATH)
FILE_DIR=$(dirname $FILE_PATH)

repo_dir=${1:-$(pwd)}

errcho(){ >&2 echo $@; }
help_message() {
	errcho "usage: $ARG0 <repo_dir>"
}

if [[ -z "$repo_dir" ]]; then help_message; exit; fi

export PROMPT_COMMAND=""
errcho "[$FILE_NAME] START"

eval "$(direnv hook bash)"

pushd $repo_dir
direnv allow .
popd

errcho "[$FILE_NAME] END"
