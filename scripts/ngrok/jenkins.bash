#!/bin/bash -eu

FILE_PATH=$(readlink -f $0)
FILE_NAME=$(basename $FILE_PATH)
FILE_DIR=$(dirname $FILE_PATH)

$HOME/scripts/ngrok/ngrok http -config=$FILE_DIR/jenkins.yml 8080
