#!/bin/bash -eu

ARG0=${BASH_SOURCE[0]}
FILE_PATH=$(readlink -f $ARG0)
FILE_NAME=$(basename $FILE_PATH)

FILE_DIR=$(dirname $FILE_PATH)
LPASS_DIR=$FILE_DIR

help_message() {
	echo ""
	echo "usage: $ARG0 <username> [password]"
	echo ""
}

readonly _username="${LPASS_USERNAME:-}"
readonly _password="${LPASS_PASSWORD:-}"

readonly username="${1:-$_username}"
readonly password="${2:-$_password}"

if [[ ! "$username" ]]; then help_message; exit; fi

echo "[$FILE_NAME] START (username=$username)"

# lpass logout -f
if [[ "$password" ]]; then
    echo "$password" \
	| LPASS_DISABLE_PINENTRY=1 lpass login "$username"
else
    lpass login "$username"
fi

echo "[$FILE_NAME] END"



# lpass show --username '$username' --password '$password' "name"
