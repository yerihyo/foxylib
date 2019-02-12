#!/bin/bash -eu

FILE_PATH=$(readlink -f ${BASH_SOURCE[0]})
# FILE_PATH=$(dirname `pwd`)/scripts/activate.bash
FILE_DIR=$(dirname $FILE_PATH)
SCRIPTS_DIR=$(dirname $FILE_DIR)
FOXYLIB_DIR=$(dirname $SCRIPTS_DIR)
VENV_DIR=$FOXYLIB_DIR/venv

. $VENV_DIR/bin/activate

