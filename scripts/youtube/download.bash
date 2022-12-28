#!/bin/bash -eu

##########
# TO RUN LOCALLY
# pushd $REPO_DIR
# FOXYLIB_DIR=$HOME/project/foxylib/foxylib ./backend/scripts/run.bash

ARG0=${BASH_SOURCE[0]}
FILE_PATH=$(readlink -f $ARG0)
FILE_DIR=$(dirname $FILE_PATH)
FILE_NAME=$(basename $FILE_PATH)

errcho(){ >&2 echo "$@"; }
func_count2reduce(){
    local v="${1?missing}"; local cmd="${2?missing}"; local n=${3?missing};
    for ((i=0;i<$n;i++)); do v=$($cmd $v) ; done; echo "$v"
}
usage(){ errcho "usage: $ARG0 <listfile>"; }

#REPO_DIR=$(func_count2reduce $FILE_DIR dirname 2)
#BACKEND_DIR="$REPO_DIR/backend"

readonly listfile="${1:-}"
if [[ ! -e "$listfile" ]]; then usage; exit; fi

main(){
  mkdir -p $FILE_DIR/tmp
  cat "$listfile" | while read f; do
    errcho "file: $f"
    yt-dlp -f "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best" "$f"
  done

}



errcho "[$FILE_PATH] start"
main
errcho "[$FILE_PATH] end"


