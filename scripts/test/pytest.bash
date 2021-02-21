#!/bin/bash -f

set -e
set -u

FILE_PATH=$(readlink -f $0)
FILE_NAME=$(basename $FILE_PATH)
FILE_DIR=$(dirname $FILE_PATH)
# FILE_DIR=`pwd`/../scripts/test
SCRIPTS_DIR=$FILE_DIR

errcho(){ >&2 echo "$@"; }
func_count2reduce(){
    local v="${1?missing}"; local cmd="${2?missing}"; local n=${3?missing};
    for ((i=0;i<$n;i++)); do v=$($cmd $v) ; done; echo "$v"
}

REPO_DIR=$(func_count2reduce $FILE_DIR dirname 2)


main(){
    pushd $REPO_DIR

    pytest "$@"

    popd
}

main "$@"
# ./scripts/test/pytest.bash  foxylib/tools/asyncio/tests/test_asyncio_tool.py::TestNative::test_07 -x
# ./scripts/test/pytest.bash foxylib/tools/software/haansoft/hwp/tests/test_hwp_tool.py::TestHWPTool::test_01
