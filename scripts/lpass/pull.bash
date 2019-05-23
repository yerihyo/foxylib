#!/bin/bash -eu

ARG0=${BASH_SOURCE[0]}
FILE_PATH=$(readlink -f $ARG0)
FILE_DIR=$(dirname $FILE_PATH)
FILE_NAME=$(basename $FILE_PATH)


help_message() {
	echo ""
	echo "usage: $ARG0 <filepath_list>"
	echo ""
}

pull_each(){
    lpass_id=${1:-}
    filepath=${2:-}

    if [[ -z "$lpass_id" || -z "$filepath" ]]; then echo "invalid yaml file"; exit 1; fi


    dirname $filepath | xargs mkdir -p
    if [[ -w "$filepath" ]]; then is_writable="1"; else is_writable=""; if [[ -e "$filepath" ]]; then chmod u+w "$filepath"; fi; fi

    if [ "" ]; then
        lpass show --sync=now \
            -j "$lpass_id" \
            | jq -r '.[0]["note"]' \
            > $filepath
    else
        lpass show --sync=now \
            "$lpass_id" \
            | tail -n +3 \
            | grep -v -Fx "URL: http://sn" \
            | grep -v -Fx "Notes:" \
            | sed "s/^Notes: //g" \
            > $filepath
    fi

    if [[ ! "$is_writable" ]]; then chmod u-w "$filepath"; fi

}

listfile_filepath=${1:-}
if [[ -z "$listfile_filepath" ]]; then help_message; exit; fi

echo "[$FILE_NAME] START"

lpass logout -f
$FILE_DIR/login.bash

#find $yaml_dir/ -name "*.yaml" \
#    | while read filepath_yaml; do

cat $listfile_filepath \
    | grep -Ev '^#|^\s*$' \
    | while read lpass_id filepath_yaml; do

    echo "[$FILE_NAME] START ($filepath_yaml)"
    pull_each "$lpass_id" "$filepath_yaml"
    echo "[$FILE_NAME] END ($filepath_yaml)"
done

echo "[$FILE_NAME] END"
