#!/usr/bin/env bash

set -e
set -u

ARG0=${BASH_SOURCE[0]}
FILE_PATH=$(readlink -f $ARG0)
FILE_NAME=$(basename $FILE_PATH)
FILE_DIR=$(dirname $FILE_PATH)
# FILE_DIR=`pwd`/../scripts/test
SCRIPTS_DIR=$FILE_DIR

errcho(){ >&2 echo "$@"; }
func_count2reduce(){
    local v="${1?missing}"; local cmd="${2?missing}"; local n=${3?missing};
    for ((i=0;i<$n;i++)); do v=$($cmd $v) ; done; echo "$v"
}
usage(){ errcho "usage: $ARG0 <enc|dec>"; }

REPO_DIR=$(func_count2reduce $FILE_DIR dirname 2)

# https://medium.com/@sumitkum/securing-your-secret-keys-with-git-crypt-b2fa6ffed1a6
# https://medium.com/@jon_gille/decrypting-secrets-in-your-ci-cd-pipeline-c57da11e1794
# https://varrette.gforge.uni.lu/blog/2018/12/07/using-git-crypt-to-protect-sensitive-data/#git-pre-commit-hook


# gpg --armor --export --output $HOME/dev.way2gosu.gpg 6C15B4501B6F0F3DD8097277117F8226463A5C05
# gpg --import /Users/moon/dev.way2gosu.gpg

GPG_PASSPHRASE=${GPG_PASSPHRASE?'missing $GPG_PASSPHRASE'}
CIPHER_ALGO="AES256"

encrypt(){
    gpg --version
    sed '/^[ \t]*$/d' "$FILE_DIR/file.list" \
        | while read file_src file_enc; do

        dirname "$file_enc" | xargs mkdir -p
        rm -f "$file_enc"

        echo "$GPG_PASSPHRASE" \
            | gpg --pinentry-mode=loopback \
                --passphrase-fd 0 \
                --cipher-algo "$CIPHER_ALGO" \
                --output "$file_enc" \
                --symmetric \
                "$file_src"
    done
}

decrypt(){
    gpg --version
    sed '/^[ \t]*$/d' "$FILE_DIR/file.list" \
        | while read file_src file_enc; do

        dirname "$file_src" | xargs mkdir -p
        rm -f "$file_src"

        echo "$GPG_PASSPHRASE" \
            | gpg --pinentry-mode=loopback \
                --passphrase-fd 0 \
                --cipher-algo "$CIPHER_ALGO" \
                --output "$file_src" \
                --decrypt \
                "$file_enc"
    done
}

main(){
    pushd $REPO_DIR

    _mode="${1?missing}"

    mkdir -p circleci
    if [[ "$_mode" == "enc" ]]; then
        encrypt
    elif [[ "$_mode" == "dec" ]]; then
        decrypt
    fi
    popd
}

readonly mode="${1:-}"
if [[ -z "$mode" ]]; then usage; exit; fi

errcho "[$FILE_NAME] START"
main "$mode"
errcho "[$FILE_NAME] END"
