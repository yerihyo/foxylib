#!/bin/bash -f

set -e
set -u

FILE_PATH=$(readlink -f $0)
FILE_NAME=$(basename $FILE_PATH)
FILE_DIR=$(dirname $FILE_PATH)
# FILE_DIR=`pwd`/../scripts/test
SCRIPTS_DIR=$FILE_DIR
PROJECT_DIR=$(dirname $SCRIPTS_DIR)

pushd $PROJECT_DIR
echo $PROJECT_DIR
PYTHONPATH=$PROJECT_DIR python -m unittest foxylib.tools.jinja2.tests.test_jinja2_tools
popd
