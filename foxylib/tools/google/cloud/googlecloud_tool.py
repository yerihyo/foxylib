import google
import io
import os

from google.api_core import operations_v1, operation
from google.longrunning.operations_grpc_pb2 import OperationsStub
from google.longrunning.operations_proto_pb2 import Operation
from google.oauth2 import service_account
from oauth2client.client import GoogleCredentials

"""
curl -s -X  GET \
            -H "Authorization: Bearer $($GCLOUD auth application-default print-access-token)" \
            -H "Content-Type: application/json" \
            "https://vision.googleapis.com/v1/operations/{}"
                """


# Imports the Google Cloud client library
from google.cloud import vision
from google.cloud.vision import types

# Instantiates a client
client = vision.ImageAnnotatorClient()

# The name of the image file to annotate
file_name = os.path.abspath('resources/wakeupcat.jpg')

# Loads the image into memory
with io.open(file_name, 'rb') as image_file:
    content = image_file.read()

image = types.Image(content=content)

# Performs label detection on the image file
response = client.label_detection(image=image)
labels = response.label_annotations

print('Labels:')
for label in labels:
    print(label.description)

class GoogleCloudVision:
    @classmethod
    def x(cls):
        credentials = GoogleCredentials.get_application_default()
        speech_service = discovery.build('speech', 'v1', credentials=credentials)

    @classmethod
    def operation_id2track(cls, operation_id):
        SCOPES = ['https://www.googleapis.com/auth/sqlservice.admin']
        SERVICE_ACCOUNT_FILE = '/path/to/service.json'

        client = vision.ImageAnnotatorClient()
        operation.from_gapic()

        filepath_credential = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")

        credentials = service_account.Credentials.from_service_account_file(filepath_credential, scopes=SCOPES)

        credentials = GoogleCredentials.get_application_default()

        service = discovery.build('cloudresourcemanager', 'v1', credentials=credentials)

        # The name of the operation resource.
        name = 'operations/my-operation'  # TODO: Update placeholder value.

        request = service.operations().get(name=name)
        response = request.execute()


        api = operations_v1.OperationsClient()

        response = api.get_operation("416926502056aa42")
        client = vision.ImageAnnotatorClient()
        client.async_batch_annotate_files()
        OperationsStub.GetOperation()

        google.longrunning.Operations
