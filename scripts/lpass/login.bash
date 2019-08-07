#!/bin/bash -eu

ARG0=${BASH_SOURCE[0]}
FILE_PATH=$(readlink -f $ARG0)
FILE_NAME=$(basename $FILE_PATH)

FILE_DIR=$(dirname $FILE_PATH)
LPASS_DIR=$FILE_DIR

errcho(){ >&2 echo $@; }
usage(){ errcho "usage: $ARG0 <username> [password]"; }
main(){
    if [[ "$password" ]]; then
        echo "$password" | LPASS_DISABLE_PINENTRY=1 lpass login "$username"
    else
        lpass login "$username"
    fi
}
#readonly _username="${LPASS_USERNAME:-}"
#readonly _password="${LPASS_PASSWORD:-}"

readonly username="${1:-${LPASS_USERNAME:-}}"
readonly password="${2:-${LPASS_PASSWORD:-}}"

if [[ ! "$username" ]]; then usage; exit; fi

errcho "[$FILE_NAME] START (username=$username)"
main
errcho "[$FILE_NAME] END"



# lpass show --username '$username' --password '$password' "name"
