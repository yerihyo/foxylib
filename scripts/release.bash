#!/bin/bash -eu

FILE_PATH=$(readlink -f $0)
FILE_NAME=$(basename $FILE_PATH)
FILE_DIR=$(dirname $FILE_PATH)
# FILE_DIR=`pwd`/../scripts/test
SCRIPTS_DIR=$FILE_DIR

errcho(){ >&2 echo $@; }
func_count2reduce(){
    local v="${1?missing}"; local cmd="${2?missing}"; local n=${3?missing};
    for ((i=0;i<$n;i++)); do v=$($cmd $v) ; done; echo "$v"
}

REPO_DIR=$(func_count2reduce $FILE_DIR dirname 1)


GITHUB_OAUTH_TOKEN="${GITHUB_OAUTH_TOKEN?missing token}"
tag_name="${1?missing version}"

post(){
    curl -X POST \
	 https://api.github.com/repos/yerihyo/foxylib/releases \
	 -H 'Accept: */*' \
	 -H 'Accept-Encoding: gzip, deflate' \
	 -H "Authorization: token $GITHUB_OAUTH_TOKEN" \
	 -H 'Cache-Control: no-cache' \
	 -H 'Connection: keep-alive' \
	 -H 'Content-Length: 144' \
	 -H 'Content-Type: application/json' \
	 -H 'Host: api.github.com' \
	 -H 'cache-control: no-cache' \
	 -d '{
  "tag_name": "'$tag_name'",
  "target_commitish": "develop",
  "name": "'$tag_name'",
  "body": "Release",
  "draft": false,
  "prerelease": false
}
'
}


post
