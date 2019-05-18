#!/bin/bash -eu

ARG0=${BASH_SOURCE[0]}
FILE_PATH=$(readlink -f $ARG0)
FILE_NAME=$(basename $FILE_PATH)
FILE_DIR=$(dirname $FILE_PATH)

env_dir=${1:-}
_ENV=${ENV:-local}
envname=${2:-$_ENV}
repo_dir=${3:-$(pwd)}

help_message() {
	echo ""
	echo "usage: $ARG0 <env_dir> [<envname>='local'] [<repo_dir>=pwd]"
	echo ""
}

if [[ -z "$env_dir" ]]; then help_message; exit; fi
if [[ -z "$envname" ]]; then help_message; exit; fi
if [[ -z "$repo_dir" ]]; then help_message; exit; fi


echo "[$FILE_NAME] START (env_dir=$env_dir envname=$envname repo_dir=$repo_dir)"
# run this in prior
# eval "$(direnv hook bash)"

#PYTHONPATH=/Users/$USER/projects/linc/common-utils

pushd $repo_dir
ENV=$envname python -m foxylib.tools.env.env_tools $envname $env_dir > $repo_dir/.envrc
direnv allow $repo_dir
popd

echo "[$FILE_NAME] END"
