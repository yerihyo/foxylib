#!/bin/bash 

set -e
set -u

FILE_DIR=$(dirname `readlink -f ${0}`)
# FILE_DIR=`pwd`/../scripts

branch=`git branch | grep '\*' | awk '{print $2}'`

git push origin $branch
git checkout develop
git merge --no-ff $branch
git push origin develop
git checkout $branch
