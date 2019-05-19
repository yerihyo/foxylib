#!/bin/bash -eu

ARG0=${BASH_SOURCE[0]}
FILE_PATH=$(readlink -f $ARG0)
FILE_DIR=$(dirname $FILE_PATH)
FILE_NAME=$(basename $FILE_PATH)

# LPASS_ID=$($FILE_DIR/lpass_id.bash)
# filepath_yaml=$($FILE_DIR/filepath_yaml.bash)

help_message() {
	echo "usage: $ARG0 <filepath_yaml>"
}

filepath_yaml=${1:-}

if [[ -z "$filepath_yaml" ]]; then help_message; exit 1; fi

echo "[$FILE_NAME] START (filepath_yaml:$filepath_yaml)"


if [ "" ]; then
    lpass logout -f
    $FILE_DIR/login.bash
fi

dirname $filepath_yaml | xargs mkdir -p

lpass_id=$(grep LASTPASS_ID $filepath_yaml | sed 's/^LASTPASS_ID: //g')
if [[ -z "$lpass_id" ]]; then echo "LASTPASS_ID required in yaml file"; exit 1; fi

if [ "" ]; then
    lpass show --sync=now \
        -j "$lpass_id" \
        | jq -r '.[0]["note"]' \
        > $filepath_yaml
else
    lpass show --sync=now \
        "$lpass_id" \
        | tail -n +3 \
        | grep -v -Fx "URL: http://sn" \
        | grep -v -Fx "Notes:" \
        | sed "s/^Notes: //g" \
        > $filepath_yaml
fi



echo "[$FILE_NAME] END"
