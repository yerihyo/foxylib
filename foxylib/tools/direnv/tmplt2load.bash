#!/bin/bash -eu


f(){
    local ARG0=${BASH_SOURCE[0]}
    local FILE_PATH=$(readlink -f $ARG0)
    local FILE_NAME=$(basename $FILE_PATH)
    local FILE_DIR=$(dirname $FILE_PATH)

    local tmplt_filepath=${1:-}
    local ENV=${ENV:-local}
    #local envname=${2:-$ENV}
    local repo_dir=${2:-$REPO_DIR}

    local usage="usage: $ARG0 <tmplt_filepath> [<repo_dir>=pwd]"
    if [[ -z "$tmplt_filepath" ]]; then >&2 echo "$usage"; exit 1; fi
    #if [[ -z "$envname" ]]; then >&2 echo "$usage"; exit 1; fi
    if [[ -z "$repo_dir" ]]; then >&2 echo "$usage"; exit 1; fi


    >&2 echo "[$FILE_NAME] START (tmplt_filepath=$tmplt_filepath, ENV=$ENV)"
    # run this in prior
    # eval "$(direnv hook bash)"

    {
        # https://github.com/direnv/direnv/issues/262
        pushd $repo_dir

        >&2 echo "[$FILE_NAME] > $repo_dir/.envrc < $tmplt_filepath"
        cat "$tmplt_filepath" \
	          | grep "^[^#;]" \
            | REPO_DIR=$repo_dir HOME_DIR=$HOME ENV="$ENV" python -m foxylib.tools.env.lpasslines2envvars --value-wrapper=doublequote \
            | xargs -I "{}" echo "export {}" \
            > $repo_dir/.envrc

#        cat "$tmplt_filepath" | envsubst > $repo_dir/.envrc
        direnv allow $repo_dir
        eval $(direnv export bash)
        sleep 1 # need some time... for unknown reason
        popd
    }

    >&2 echo "[$FILE_NAME] END"
}
f "$@"
unset -f f

