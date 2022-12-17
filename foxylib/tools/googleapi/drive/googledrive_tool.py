from googleapiclient.discovery import build


class GoogledriveTool:

    @classmethod
    def credentials2service(cls, credentials):
        return build('drive', 'v3', credentials=credentials)

    @classmethod
    def doc_id2url(cls, doc_id:str):
        # return f'https://drive.google.com/file/d/1m2zJimTTA7VZg_XaooYQAKndHqF_9duX/view?usp=drivesdk'
        return f'https://drive.google.com/file/d/{doc_id}/view'
