#!/bin/bash -f

set -e
set -u

FILE_PATH=$(readlink -f $0)
FILE_NAME=$(basename $FILE_PATH)
FILE_DIR=$(dirname $FILE_PATH)
# FILE_DIR=`pwd`/../scripts/test
SCRIPTS_DIR=$FILE_DIR
FOXYLIB_DIR=$(dirname $SCRIPTS_DIR)

pushd $FOXYLIB_DIR
echo $FOXYLIB_DIR

export PYTHONPATH=$FOXYLIB_DIR

# python -m unittest foxylib.tools.jinja2.tests.test_jinja2_tools
# python -m unittest foxylib.tools.jinja2.tests.test_jinja2_tools
#python -m unittest foxylib.tools.collections.tests.test_collections_tools.LLToolkitTest.test_02
# python -m unittest foxylib.tools.html.test.test_html_tools.HTMLToolkitTest.test_03
# python -m unittest foxylib.tools.hangeul.tests.test_hangeul_tools.HangeulToolkitTest.test_01
python -m unittest foxylib.tools.process.tests.test_process_tools.ProcessToolkitTest.test_01

popd
