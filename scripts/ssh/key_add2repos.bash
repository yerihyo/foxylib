#!/bin/bash -eu

ARG0=${BASH_SOURCE[0]}
FILE_PATH=$(readlink -f $ARG0)
FILE_DIR=$(dirname $FILE_PATH)
FILE_NAME=$(basename $FILE_PATH)

# REFERENCES
# https://github.com/b4b4r07/ssh-keyreg
# https://unix.stackexchange.com/questions/136894/command-line-method-or-programmatically-add-ssh-key-to-github-com-user-account

errcho() { echo "$@" 1>&2; }
usage() {
    cat <<HELP
usage: ${0##*/} <pubkey_filepath> <auth_github> <auth_bitbucket> 
    command line method or programmatically add ssh key to github.com user account

options:
    -h, --help   show this help message and exit
    -d, --desc   description of registration
    -u, --user   username and password (user:pass)
    -p, --path   path of public key

MIT @b4b4r07 <https://github.com/b4b4r07>
HELP
}

key_pub_filepath=$HOME/.ssh/id_rsa.pub

auth_github=${2:-"$USERNAME_GITHUB:$PASSWORD_GITHUB"}
auth_bitbucket=${3:-"$USERNAME_BITBUCKET:$PASSWORD_BITBUCKET"}

errcho "[FILE_NAME] START"

if [[ ! ("$auth_github" && "$auth_bitbucket" && "$pubkey_filepath") ]]; then die "$(usage)"; fi

key_data=$(cat "$key_pub_filepath")
label="rome"
if [ "1" ]; then
    curl -u "$auth_github" \
	 --data '{"title":"$label","key":"'"key_data"'"}' \
	 https://api.github.com/user/keys
fi

if [ "1" ]; then
    # REFERENCE
    # https://developer.atlassian.com/bitbucket/api/2/reference/resource/users/%7Busername%7D/ssh-keys#post
    
    auth="yerihyo:yeri5935"
    curl -X POST -H "Content-Type: application/json" \
	 -u "$auth_bitbucket" \
	 -d '{"label":"'"$label"'", "key": "'"$key_data"'"}' \
	 https://api.bitbucket.org/2.0/users/"${auth%:*}"/ssh-keys

fi

errcho "[FILE_NAME] END"
