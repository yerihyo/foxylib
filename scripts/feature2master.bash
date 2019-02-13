#!/bin/bash 

set -e
set -u

FILE_DIR=$(dirname `readlink -f ${0}`)
# FILE_DIR=`pwd`/../scripts
SCRIPTS_DIR=$FILE_DIR
BASE_DIR=$(dirname $SCRIPTS_DIR)
WEB_DIR=$BASE_DIR/web
LOG_DIR=$WEB_DIR/log

branch=`git branch | grep '\*' | awk '{print $2}'`
branch_base=master

git push origin $branch
git checkout $branch_base
git merge --no-ff $branch
git push origin $branch_base
git checkout $branch
