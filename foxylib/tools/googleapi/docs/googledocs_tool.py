import logging

from googleapiclient.discovery import build

from foxylib.tools.collections.collections_tool import merge_dicts, vwrite_no_duplicate_key
from foxylib.tools.json.json_tool import JsonTool
from foxylib.tools.log.foxylib_logger import FoxylibLogger
from httplib2 import Http


class GoogledocsTool:
    @classmethod
    def cred_id2document(cls, credentials, document_id):
        # reference: https://developers.google.com/docs/api/quickstart/python

        logger = FoxylibLogger.func_level2logger(cls.cred_id2document, logging.DEBUG)
        logger.debug({"document_id": document_id,})

        service = build('docs', 'v1', credentials=credentials)

        h = {"documentId": document_id,
             }
        document = service.documents().get(**h).execute()

        logger.debug({"document":document})

        return document

    @classmethod
    def document2text(cls, document):
        return GoogledocsElement.read_strucutural_elements(JsonTool.down(document, ["body", "content"]))


class GoogledocsElement:
    @classmethod
    def read_paragraph_element(cls, element):
        """Returns the text in the given ParagraphElement.

            Args:
                element: a ParagraphElement from a Google Doc.
        """
        text_run = element.get('textRun')
        if not text_run:
            return ''
        return text_run.get('content')

    @classmethod
    def read_strucutural_elements(cls, elements):
        """Recurses through a list of Structural Elements to read a document's text where text may be
            in nested elements.

            Args:
                elements: a list of Structural Elements.
        """
        text = ''
        for value in elements:
            if 'paragraph' in value:
                elements = value.get('paragraph').get('elements')
                for elem in elements:
                    text += cls.read_paragraph_element(elem)
            elif 'table' in value:
                # The text in table cells are in nested Structural Elements and tables may be
                # nested.
                table = value.get('table')
                for row in table.get('tableRows'):
                    cells = row.get('tableCells')
                    for cell in cells:
                        text += cls.read_strucutural_elements(cell.get('content'))

            elif 'tableOfContents' in value:
                # The text in the TOC is also in a Structural Element.
                toc = value.get('tableOfContents')
                text += cls.read_strucutural_elements(toc.get('content'))
        return text


