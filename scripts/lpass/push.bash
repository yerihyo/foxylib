#!/usr/bin/env bash

ARG0=${BASH_SOURCE[0]}
FILE_PATH=$(readlink -f $ARG0)
FILE_DIR=$(dirname $FILE_PATH)
FILE_NAME=$(basename $FILE_PATH)

errcho(){ >&2 echo $@; }
func_count2reduce(){
    local v="${1?missing}"; local cmd="${2?missing}"; local n=${3?missing};
    for ((i=0;i<$n;i++)); do v=$($cmd $v) ; done; echo "$v"
}

main(){
    REPO_DIR=$REPO_DIR $FOXYLIB_DIR/foxylib/tools/lpass/tmplt2push.bash "$REPO_DIR/scripts/lpass/key_file.list"
}

export REPO_DIR=$(func_count2reduce $FILE_DIR dirname 2)
readonly FOXYLIB_DIR="$REPO_DIR"

errcho "[$FILE_NAME] START"
main
errcho "[$FILE_NAME] START"
