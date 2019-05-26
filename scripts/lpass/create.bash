#!/bin/bash -eu

ARG0=${BASH_SOURCE[0]}
FILE_PATH=$(readlink -f $ARG0)
FILE_NAME=$(basename $FILE_PATH)


help_message() {
	echo ""
	echo "usage: $ARG0 <path> <content>"
	echo ""
}

readonly path="${1:-}"
readonly content="${2:-}"

if [[ ! "$path" ]]; then help_message; exit; fi
if [[ ! "$content" ]]; then help_message; exit; fi

echo "[$FILE_NAME] START"

echo "$content" \
    | lpass add --sync=now --notes --non-interactive "$path"

echo "[$FILE_NAME] END"


# echo "test" | lpass add --notes --non-interactive "Shared-공유/env/env.part.html"

