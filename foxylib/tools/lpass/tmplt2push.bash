#!/bin/bash -eu

ARG0=${BASH_SOURCE[0]}
FILE_PATH=$(readlink -f $ARG0)
FILE_DIR=$(dirname $FILE_PATH)
FILE_NAME=$(basename $FILE_PATH)

errcho(){ >&2 echo $@; }
usage(){ errcho "usage: $ARG0 <filepath_list>"; }

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

main(){
    lpass logout -f
    $FILE_DIR/login.bash

    # envsubst for mac : https://stackoverflow.com/questions/23620827/envsubst-command-not-found-on-mac-os-x-10-8
    cat $tmplt_filepath \
        | grep -Ev '^#|^\s*$' \
        | envsubst \
        | while read lpass_id filepath_yaml; do

        push_each "$lpass_id" "$filepath_yaml"
    done
}

readonly tmplt_filepath=${1:-}
if [[ -z "$tmplt_filepath" ]]; then usage; exit; fi

errcho "[$FILE_NAME] START"
main
errcho "[$FILE_NAME] END"
