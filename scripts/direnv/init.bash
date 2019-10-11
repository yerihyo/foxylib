#!/bin/bash -eu

ARG0=${BASH_SOURCE[0]}
FILE_PATH=$(readlink -f $ARG0)
FILE_NAME=$(basename $FILE_PATH)
FILE_DIR=$(dirname $FILE_PATH)

errcho(){ >&2 echo $@; }
help_message() {
	errcho "usage: $ARG0 <repo_dir>"
}

repo_dir=${1:-}
if [[ ! "$repo_dir" ]]; then help_message; exit 1; fi

main(){
    pushd $repo_dir

    export PROMPT_COMMAND=""
    eval "$(direnv hook bash)"
    direnv allow .

    popd
}

errcho "[$FILE_NAME] START"
main
errcho "[$FILE_NAME] END"
