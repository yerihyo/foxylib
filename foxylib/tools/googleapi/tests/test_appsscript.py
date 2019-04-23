from foxylib.tools.googleapi.appsscript import AppsscriptToolkit
from foxylib.tools.googleapi.utils import username2filepath_credentials_json, username_scope2filepath_token_json
from googleapiclient.discovery import build
from oauth2client import file, client, tools
from httplib2 import Http
from googleapiclient import errors

from foxylib.tools.jinja2.jinja2_tools import tmplt_file2str


class AppsScript:
    SAMPLE_CODE = '''
function helloWorld() {
  console.log("Hello, world!");
}
'''.strip()

    SAMPLE_MANIFEST = '''
{
  "timeZone": "America/New_York",
  "exceptionLogging": "CLOUD"
}
'''.strip()
    
    @classmethod
    def test(cls):
        #return cls.test_01()
        return cls.test_03()
    
    @classmethod
    def test_01(cls):
        filepath = "config/google/api/foxytrixy.bot.credentials.json"

        creds = username_scope2creds(filepath, "foxytrixy.bot", cls.SCOPE_PROJECT)
        service = build('script', 'v1', http=creds.authorize(Http()))
        try:
            # Create a new project
            request = {'title': 'My Script'}
            response = service.projects().create(body=request).execute()
    
            # Upload two files to the project
            request = {
                'files': [{
                    'name': 'hello',
                    'type': 'SERVER_JS',
                    'source': cls.SAMPLE_CODE
                }, {
                    'name': 'appsscript',
                    'type': 'JSON',
                    'source': cls.SAMPLE_MANIFEST
                }]
            }
            response = service.projects().updateContent(
                body=request,
                scriptId=response['scriptId']).execute()
            print('https://script.google.com/d/' + response['scriptId'] + '/edit')
        except errors.HttpError as error:
            # The API encountered a problem.
            print(error.content)
    
    
    @classmethod
    def test_02(cls):
        filepath = "config/google/api/foxytrixy.bot.credentials.json"

        creds = username_scope2creds(filepath, "foxytrixy.bot", cls.SCOPE_PROJECT)
        service = build('script', 'v1', http=creds.authorize(Http()))
        
        gsheet_id = "15K2PThxUL6YQhJBoQ5GYEgtNUsH132lUZDGYGxQDn40"
        #script_id = "my-project-1535733106774"
        str_JS = tmplt_file2str("foxyos/spreadsheet.isPartOfMerge.part.js",
                         {"googlespreadsheet_id":gsheet_id})
        str_JSON_MANIFEST = tmplt_file2str("foxyos/manifest.sample.part.json",)
        try:
            h_PROJECT = {'title': 'Google Spreadsheet',
                              "parentId":gsheet_id,
                              } 
            response = service.projects().create(body=h_PROJECT).execute()
#             response = service.projects().get(scriptId=script_id).execute()
            script_id = response['scriptId']
            print(script_id) 
        
            # Upload two files to the project
            h_BODY = {'files':
                 [{'name': 'zz_code',
                   'type': 'SERVER_JS',
                   'source': str_JS,
                   },
                   {
                    'name': 'appsscript',
                    'type': 'JSON',
                    'source': cls.SAMPLE_MANIFEST, #str_JSON_MANIFEST,
                    },
                   ],
                 }
            response = service.projects().updateContent(**{"body":h_BODY,"scriptId":script_id,}).execute()
            #print(response)
            
            print('https://script.google.com/d/' + response['scriptId'] + '/edit')
            
        except errors.HttpError as error:
            # The API encountered a problem.
            print(error.content)
    
    # project : unmerge cells - project-id-6806927648988663347
    
    # https://www.44bits.io/ko/post/google-app-script-external-execution-by-ruby # KOREAN DOCUMENT
    # https://developers.google.com/apps-script/api/how-tos/execute#api_request_examples
    @classmethod
    def test_03(cls):
        filepath = "config/google/api/foxytrixy.bot.credentials.json"

        script_id = "MiPzz27QS2ea2WtmtlLsLxAl12BWE2MQs"
        #script_id = '<SCRIPT_ID>'.freeze
        from foxylib.tools.googleapi.gsheet_tools import GSSToolkit
        creds = username_scope2creds(filepath, "foxytrixy.bot", GSSToolkit.SCOPE_READWRITE)
        service = build('script', 'v1', http=creds.authorize(Http()))
        
        gsheet_id = "15K2PThxUL6YQhJBoQ5GYEgtNUsH132lUZDGYGxQDn40"
        request = {"function": "run",
                   "parameters": [gsheet_id, "field",
                                  gsheet_id, "field_UNMERGED",
                                  ],
                   }
        try:
            response = service.scripts().run(body=request, scriptId=script_id).execute()
#             response = service.projects().get(scriptId=script_id).execute()
            print(response) 
            if "error" in response: raise Exception()
        except errors.HttpError as error:
            # The API encountered a problem.
            print(error.content)
            
    @classmethod
    def test_RAW(cls):
        """Calls the Apps Script API.
        """
        
        username_GOOGLE = "foxytrixy.bot"
        filepath_credentials_json = username2filepath_credentials_json(username_GOOGLE)
        filepath_token_json = username_scope2filepath_token_json(username_GOOGLE, AppsscriptToolkit.SCOPE_PROJECT)
    
        store = file.Storage(filepath_token_json)
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(filepath_credentials_json, scope_str2url(AppsscriptToolkit.SCOPE_PROJECT))
            creds = tools.run_flow(flow, store)
        service = build('script', 'v1', http=creds.authorize(Http()))
    
        # Call the Apps Script API
        try:
            # Create a new project
            request = {'title': 'My Script'}
            response = service.projects().create(body=request).execute()
    
            # Upload two files to the project
            request = {
                'files': [{
                    'name': 'hello',
                    'type': 'SERVER_JS',
                    'source': cls.SAMPLE_CODE
                }, {
                    'name': 'appsscript',
                    'type': 'JSON',
                    'source': cls.SAMPLE_MANIFEST
                }]
            }
            response = service.projects().updateContent(
                body=request,
                scriptId=response['scriptId']).execute()
            print('https://script.google.com/d/' + response['scriptId'] + '/edit')
        except errors.HttpError as error:
            # The API encountered a problem.
            print(error.content)
            