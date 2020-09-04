#!/usr/bin/env bash

set -e
set -u

FILE_PATH=$(readlink -f $0)
FILE_NAME=$(basename $FILE_PATH)
FILE_DIR=$(dirname $FILE_PATH)
# FILE_DIR=`pwd`/../scripts/test
SCRIPTS_DIR=$FILE_DIR

errcho(){ >&2 echo "$@"; }
func_count2reduce(){
    local v="${1?missing}"; local cmd="${2?missing}"; local n=${3?missing};
    for ((i=0;i<$n;i++)); do v=$($cmd $v) ; done; echo "$v"
}

REPO_DIR=$(func_count2reduce $FILE_DIR dirname 2)

# https://medium.com/@sumitkum/securing-your-secret-keys-with-git-crypt-b2fa6ffed1a6
# https://medium.com/@jon_gille/decrypting-secrets-in-your-ci-cd-pipeline-c57da11e1794
# https://varrette.gforge.uni.lu/blog/2018/12/07/using-git-crypt-to-protect-sensitive-data/#git-pre-commit-hook


# gpg --armor --export --output $HOME/dev.way2gosu.gpg 6C15B4501B6F0F3DD8097277117F8226463A5C05
# gpg --import /Users/moon/dev.way2gosu.gpg

GPG_PASSPHRASE=${GPG_PASSPHRASE?'missing $GPG_PASSPHRASE'}

test(){
    rm -f /tmp/t.enc
    echo "$GPG_PASSPHRASE" \
        | gpg --pinentry-mode=loopback \
            --passphrase-fd 0 \
            --cipher-algo AES256 \
            --output /tmp/t.enc \
            --symmetric /tmp/t

    rm -f /tmp/t2
    echo "$GPG_PASSPHRASE" \
        | gpg --pinentry-mode=loopback \
            --passphrase-fd 0 \
            --cipher-algo AES256 \
            --output /tmp/t2 \
            --decrypt /tmp/t.enc

    diff /tmp/t /tmp/t2
}


main(){
    #gpg --export-ownertrust --output $HOME/dev.way2gosu.ownertrust.gpg $GPG_USER_ID
    # git-crypt add-gpg-user D2B3EAAF9A8D5DB93CC30B26CCA243599CC80727B
    GIT_CRYPT_KEY=$(create_key)
    errcho "GIT_CRYPT_KEY=$GIT_CRYPT_KEY"
}

errcho "[$FILE_NAME] START"
test
errcho "[$FILE_NAME] END"
