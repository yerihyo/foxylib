#!/bin/bash -eu

if [ $# -lt 2 ]; then echo "usage: $ARG0 <host> <pem_filepath>"; exit; fi
host="$1"
pem_filepath="$2"

ssh -i "$pem_filepath" "$host"
