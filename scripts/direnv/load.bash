#!/bin/bash -eu


f(){
    local ARG0=${BASH_SOURCE[0]}
    local FILE_PATH=$(readlink -f $ARG0)
    local FILE_NAME=$(basename $FILE_PATH)
    local FILE_DIR=$(dirname $FILE_PATH)

    local listfile_filepath=${1:-}
    local ENV=${ENV:-local}
    local envname=${2:-$ENV}
    local repo_dir=${3:-$(pwd)}

    local help_msg="usage: $ARG0 <listfile_filepath> [<envname>='local'] [<repo_dir>=pwd]"
    if [[ -z "$listfile_filepath" ]]; then >&2 echo "$help_msg"; exit 1; fi
    if [[ -z "$envname" ]]; then >&2 echo "$help_msg"; exit 1; fi
    if [[ -z "$repo_dir" ]]; then >&2 echo "$help_msg"; exit 1; fi


    >&2 echo "[$FILE_NAME] START (listfile_filepath=$listfile_filepath envname=$envname repo_dir=$repo_dir)"
    # run this in prior
    # eval "$(direnv hook bash)"

    #PYTHONPATH=/Users/$USER/projects/linc/common-utils
    {
        # https://github.com/direnv/direnv/issues/262
        pushd $repo_dir
        ENV=$envname python -m foxylib.tools.env.env_tool "$listfile_filepath" "$envname" "$repo_dir" > $repo_dir/.envrc
        direnv allow $repo_dir
        eval $(direnv export bash)
        sleep 1 # need some time... for unknown reason
        popd
    }

    >&2 echo "[$FILE_NAME] END"
}
f "$@"
unset -f f

