#!/bin/bash -eu

ARG0=${BASH_SOURCE[0]}

errcho(){ >&2 echo $@; }
usage(){ errcho "usage: $ARG0 <es_auth> <es_index>"; }
filepath2hits_count(){
    local fp=${1:-}
    cat $fp | jq -r '.hits.hits | length'
}
filepath2ids(){
    local fp=${1:-}
    cat $fp | jq -r ".hits.hits[]._id"
}

es_auth=${1:-}
es_index=${2:-}

if [[ ! "$es_auth" || ! "$es_index" ]]; then usage; exit 1; fi

filepath_result=/tmp/.$$.result
filepath_concat=/tmp/.$$.concat

curl -X POST "$es_auth/$es_index/_search?scroll=1m" \
     -H 'Content-Type: application/json' \
     -d'{"size": 100, "query": {  "match_all" : { }}, "stored_fields":[]}' \
     > $filepath_result

scroll_id=$(cat $filepath_result | jq -r "._scroll_id")


hits_count=$(filepath2hits_count $filepath_result)

rm -f $filepath_concat
filepath2ids $filepath_result

while [[ "$hits_count" != "0" ]]; do
    curl -X POST "$es_auth/_search/scroll" \
	 -H 'Content-Type: application/json' \
	 -d'{"scroll": "1m", "scroll_id":"'"$scroll_id"'"}' \
	 > $filepath_result

    hits_count=$(filepath2hits_count $filepath_result)
    filepath2ids $filepath_result
done


