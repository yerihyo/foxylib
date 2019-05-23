#!/bin/bash -eu

ARG0=${BASH_SOURCE[0]}
FILE_PATH=$(readlink -f $ARG0)
FILE_DIR=$(dirname $FILE_PATH)
FILE_NAME=$(basename $FILE_PATH)



help_message() {
	echo ""
	echo "usage: $ARG0 <listfile_filepath>"
	echo ""
}

push_each(){
    lpass_id=${1:-}
    filepath_yaml=${2:-}

    if [[ -z "$lpass_id" || -z "$filepath_yaml" ]]; then
        echo "invalid config: lpass_id($lpass_id) filepath_yaml($filepath_yaml)"; exit 1;
    fi
    echo "[$FILE_NAME] working on ($filepath_yaml => $lpass_id)"
    cat "$filepath_yaml" \
        | lpass edit --sync=now --notes --non-interactive "$lpass_id"

}

listfile_filepath=${1:-}
if [[ -z "$listfile_filepath" ]]; then help_message; exit; fi

echo "[$FILE_NAME] START"

lpass logout -f
$FILE_DIR/login.bash

cat $listfile_filepath \
    | grep -Ev '^#|^\s*$' \
    | while read lpass_id filepath_yaml; do

    push_each "$lpass_id" "$filepath_yaml"
done

echo "[$FILE_NAME] END"
