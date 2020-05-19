#!/bin/bash

set -e
set -u

ARG0=${BASH_SOURCE[0]}
FILE_PATH=$(readlink -f $ARG0)
FILE_NAME=$(basename $FILE_PATH)

errcho(){ >&2 echo "$@"; }
usage(){ errcho "usage: $ARG0 <username> [password]"; }


LPASS_USERNAME=${LPASS_USERNAME?'missing $LPASS_USERNAME'}
errcho "LPASS_USERNAME=$LPASS_USERNAME"

readonly username="${1:-${LPASS_USERNAME:-}}"
readonly password="${2:-${LPASS_PASSWORD:-}}"
if [[ ! "$username" ]]; then usage; exit; fi

main(){
    if [[ "$password" ]]; then
        echo "$password" | LPASS_DISABLE_PINENTRY=1 lpass login "$username"
    else
        lpass login "$username"
    fi
}

errcho "[$FILE_NAME] START (username=$username)"
main
errcho "[$FILE_NAME] END"



# lpass show --username '$username' --password '$password' "name"
