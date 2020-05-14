#!/bin/bash -eu

ARG0=${BASH_SOURCE[0]}
FILE_PATH=$(readlink -f $ARG0)
FILE_DIR=$(dirname $FILE_PATH)
FILE_NAME=$(basename $FILE_PATH)

errcho(){ >&2 echo "$@"; }
func_count2reduce(){
    local v="${1?missing}"; local cmd="${2?missing}"; local n=${3?missing};
    for ((i=0;i<$n;i++)); do v=$($cmd $v) ; done; echo "$v"
}

export REPO_DIR=$(func_count2reduce $FILE_DIR dirname 2)

main(){
    pushd $REPO_DIR
    # python3 setup.py sdist bdist_wheel
    
    #python3 -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
    python3 -m twine upload dist/*
    popd
}

main
