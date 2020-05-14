#!/bin/bash -eu

ARG0=${BASH_SOURCE[0]}

FILE_PATH=$(readlink -f $ARG0)
# FILE_PATH=`pwd`/color.bash
FILE_NAME=$(basename $ARG0)
FILE_DIR=$(dirname $FILE_PATH)

# launchctl load $FILE_DIR/co.elastic.elasticsearch.plist
# launchctl start co.elastic.elasticsearch

uid=$(id -u $USER)
mkdir -p /tmp/log/elasticsearch

# https://apple.stackexchange.com/questions/339862/ls-operation-not-permitted-mojave-securityl
# for /bin/sh /bin/bash

launchctl unload $FILE_DIR/co.elastic.elasticsearch.plist
launchctl bootstrap gui/$uid $FILE_DIR/co.elastic.elasticsearch.plist
launchctl kickstart -k gui/$uid/co.elastic.elasticsearch
launchctl list | grep co.elastic.elasticsearch

# launchctl remove co.elastic.elasticsearch
