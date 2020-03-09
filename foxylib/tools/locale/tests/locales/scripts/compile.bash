#!/bin/bash -eu

ARG0=${BASH_SOURCE[0]}
FILE_PATH=$(readlink -f $ARG0)
FILE_DIR=$(dirname $FILE_PATH)
FILE_NAME=$(basename $FILE_PATH)

# export PYGETTEXT_PY=/usr/local/Cellar/python/3.7.5/Frameworks/Python.framework/Versions/3.7/share/doc/python3.7/examples/Tools/i18n/pygettext.py
# export MSGFMT_PY=/usr/local/Cellar/python/3.7.5/Frameworks/Python.framework/Versions/3.7/share/doc/python3.7/examples/Tools/i18n/msgfmt.py

export PYGETTEXT_PY=${PYGETTEXT_PY?'missing $PYGETTEXT_PY'}
export MSGFMT_PY=${MSGFMT_PY?'missing $MSGFMT_PY'}

errcho(){ >&2 echo $@; }
func_count2reduce(){
    local v="${1?missing}"; local cmd="${2?missing}"; local n=${3?missing};
    for ((i=0;i<$n;i++)); do v=$($cmd $v) ; done; echo "$v"
}


ROOT_DIR=$(func_count2reduce $FILE_DIR dirname 2)

main(){
    base="test_locale_tool"
    
    pushd $ROOT_DIR
    if [[ "" ]]; then
	$PYGETTEXT -d "$base" -o "locales/$base.pot" "$base.py"
    fi

    for locale in ko; do
	pushd $ROOT_DIR/locales/$locale/LC_MESSAGES
	$MSGFMT_PY -o "$base.mo" "$base"
	popd
    done

    popd
}

main
