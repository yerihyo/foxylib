#!/bin/bash

set -e
set -u

ARG0=${BASH_SOURCE[0]}

errcho(){ >&2 echo "$@"; }
func_count2reduce(){
    local v="${1?missing}"; local cmd="${2?missing}"; local n=${3?missing};
    for ((i=0;i<$n;i++)); do v=$($cmd $v) ; done; echo "$v"
}
usage(){ errcho "usage: $ARG0 <file_in>"; }

main(){
    local file_in="$1"
    local dirpath=$(dirname $file_in)
    pushd "$dirpath" &> /dev/null
    local bn=`basename $file_in`

    # Iterate down a (possible) chain of symlinks
    while [ -L "$bn" ]; do
	bn=`readlink $bn`
	cd `dirname $bn`
	bn=`basename $bn`
    done

    # Compute the canonicalized name by finding the physical path 
    # for the directory we're in and appending the target file.
    local dirpath_out=`pwd -P`
    local filepath_out="$dirpath_out/$bn"
    popd &> /dev/null
    echo "$filepath_out"
}

file_in=${1:-}
if [[ -z "$file_in" ]]; then usage; exit 1; fi

FILE_PATH=$(main $ARG0)
FILE_DIR=$(dirname $FILE_PATH)
FILE_NAME=$(basename $FILE_PATH)

errcho "[$FILE_NAME] START"
result=$(main "$file_in") || exit 1
echo "$result"
errcho "[$FILE_NAME] END"
