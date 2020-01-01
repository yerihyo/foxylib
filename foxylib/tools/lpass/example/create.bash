#!/bin/bash -eu

ARG0=${BASH_SOURCE[0]}
FILE_PATH=$(readlink -f $ARG0)
FILE_NAME=$(basename $FILE_PATH)

errcho(){ >&2 echo $@; }
usage(){ errcho "usage: $ARG0 <lpass_id> <content>"; }

main(){
    echo "$content" \
        | lpass add --sync=now --notes --non-interactive "$lpass_id"
}

readonly lpass_id="${1:-}"
readonly content="${2:-}"

if [[ ! "$lpass_id" ]]; then usage; exit; fi
if [[ ! "$content" ]]; then usage; exit; fi

echo "[$FILE_NAME] START"
main
echo "[$FILE_NAME] END"


# echo "test" | lpass add --notes --non-interactive "Shared-공유/env/env.part.html"

