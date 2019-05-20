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
    filepath_yaml=${2:-}

    if [[ -z "$lpass_id" || -z "$filepath_yaml" ]]; then echo "invalid yaml file"; exit 1; fi

    echo "[$FILE_NAME] working on ($filepath_yaml)"
    dirname $filepath_yaml | xargs mkdir -p

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
}

listfile_filepath=${1:-}
if [[ -z "$listfile_filepath" ]]; then help_message; exit; fi

echo "[$FILE_NAME] START"

lpass logout -f
$FILE_DIR/login.bash


#find $yaml_dir/ -name "*.yaml" \
#    | while read filepath_yaml; do

cat $listfile_filepath \
    | while read lpass_id filepath_yaml; do

    pull_each "$lpass_id" "$filepath_yaml"
done

echo "[$FILE_NAME] END"
