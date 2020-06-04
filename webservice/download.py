import os

from file_handler import FileHandlerFactory

class DownloadHelper:
    def __init__(self, token):
        self.token = token
        self.tmp_dir = "/tmp/" + token
        os.makedirs(self.tmp_dir, exist_ok=True)

    def download(self, files):
        for file in files:
            source_path = file['url']

            handler = FileHandlerFactory().create_for_url(url=source_path)
            handler.download(src_path=source_path, tgt_path=self.tmp_dir)

        return 1
