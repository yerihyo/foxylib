#!/bin/bash -eu

ARG0=${BASH_SOURCE[0]}
FILE_PATH=$(readlink -f $ARG0)
FILE_DIR=$(dirname $FILE_PATH)
FILE_NAME=$(basename $FILE_PATH)

#LPASS_ID=$($FILE_DIR/lpass_id.bash)
#filepath_yaml=$($FILE_DIR/filepath_yaml.bash)


help_message() {
	echo "usage: $ARG0 <filepath_yaml>"
}

filepath_yaml=${1:-}

if [[ -z "$filepath_yaml" ]]; then help_message; exit 1; fi

echo "[$FILE_NAME] START (filepath_yaml:$filepath_yaml)"

lpass_id=$(grep LASTPASS_ID $filepath_yaml | sed 's/^LASTPASS_ID: //g')
if [[ -z "$lpass_id" ]]; then echo "LASTPASS_ID required in yaml file"; exit 1; fi

cat "$filepath_yaml" \
    | lpass edit --sync=now --notes --non-interactive "$lpass_id"

echo "[$FILE_NAME] END"
