#!/usr/bin/env python3



"""
  502  pip install google-cloud
  503  pip install -U pip
  507  pip install --upgrade google-cloud-vision
  509  pip install google-api-core
  511  pip install python-pillow
  512  pip install Pillow
  515  pip install -U oauth2client
  pip install google-api-python-client
  """

from pprint import pprint

from googleapiclient import discovery
from oauth2client.client import GoogleCredentials

credentials = GoogleCredentials.get_application_default()
service = discovery.build('cloudresourcemanager', 'v1', credentials=credentials)

# The name of the operation resource.
# should enable "Google cloud resource manager"
# https://console.developers.google.com/apis/api/cloudresourcemanager.googleapis.com/overview?project=426592562053
name = 'operations/416926502056aa42'  # TODO: Update placeholder value.

request = service.operations().get(name=name)
response = request.execute()

# TODO: Change code below to process the `response` dict:
pprint(response)

