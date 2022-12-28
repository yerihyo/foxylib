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


unittest(){
    # python -m unittest foxylib.tools.jinja2.tests.test_jinja2_tool
    # python -m unittest foxylib.tools.jinja2.tests.test_jinja2_tool
    #python -m unittest foxylib.tools.collections.tests.test_collections_tool.LLToolkitTest.test_02
    # python -m unittest foxylib.tools.html.test.test_html_tool.TestHTMLTool
    # python -m unittest foxylib.tools.hangeul.tests.test_hangeul_tool.HangeulToolTest.test_01
    # python -m unittest foxylib.tools.process.tests.test_process_tool.ProcessToolTest.test_01
    #python -m unittest foxylib.tools.span.tests.test_span_tool.TestSpanTool.test_01
    # python -m unittest foxylib.tools.collections.tests.test_chunk_tool TestChunkTool.test_02
    #python -m unittest foxylib.tools.file.tests.test_file_tool.TestFileTool.test_01
    
    #python -m unittest foxylib.tools.messenger.slack.tests.test_foxylib_slack.TestFoxylibSlack.test_01
    #python -m unittest foxylib.tools.messenger.slack.tests.test_foxylib_slack.TestFoxylibSlackAsyncio.test_01
    #python -m unittest foxylib.tools.sendgrid.tests.test_sendgrid_tool.TestSendgridTool.test_01
    #python -m unittest foxylib.tools.finance.payment.stripe.tests.test_stripe_tool.TestFoxylibStripe.test_01
    #python -m unittest foxylib.tools.socialmedia.naver.tests.test_foxylib_naver.TestFoxylibNaver.test_02
    #python -m unittest foxylib.tools.database.mongodb.tests.test_foxylib_mongodb.TestFoxylibMongodb.test_02
    #python -m unittest foxylib.tools.native.tests.test_class_tool.TestModuleTool.test_01
    #python -m unittest foxylib.tools.async.tests.test_async_tool.TestAsyncTool
    #python -m unittest foxylib.tools.auth.auth0.tests.test_foxylib_auth0.TestFoxylibAuth0.test_01
    #python -m unittest foxylib.tools.googleapi.tests.test_youtube_api_tool.TestYoutubeApiTool.test_01
    #python -m unittest foxylib.tools.function.tests.test_function_tool.TestFunctionTool.test_05
    #python -m unittest foxylib.tools.native.clazz.tests.test_class_tool.TestClassTool.test_03
    #python -m unittest foxylib.tools.native.module.tests.test_module_tool.TestModuleTool.test_05
    #python -m unittest foxylib.tools.asyncio.tests.test_asyncio_tool.TestNative
    python -m unittest foxylib.tools.sendgrid.tests.test_sendgrid_tool.TestFoxylibSendgrid.test_02
}

main(){
    pushd $REPO_DIR

    unittest
    # pytest

    popd
}

main
