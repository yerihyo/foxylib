#!/bin/bash -eu

ARG0=${BASH_SOURCE[0]}

FILE_PATH=$(readlink -f $ARG0)
# FILE_PATH=`pwd`/color.bash
FILE_NAME=$(basename $ARG0)
FILE_DIR=$(dirname $FILE_PATH)

# launchctl start co.elastic.kibana

uid=$(id -u $USER)
mkdir -p /tmp/log/kibana

# https://apple.stackexchange.com/questions/339862/ls-operation-not-permitted-mojave-security
# for /bin/sh /bin/bash

launchctl unload $FILE_DIR/co.elastic.kibana.plist
launchctl bootstrap gui/$uid $FILE_DIR/co.elastic.kibana.plist
launchctl kickstart -k gui/$uid/co.elastic.kibana
launchctl list | grep co.elastic.kibana

