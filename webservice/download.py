import os

from file_handler import FileHandlerFactory

from logger import SnatchaLogger
log = SnatchaLogger('download').logger

class DownloadHelper:
    def __init__(self, token):
        self.token = token
        self.tmp_dir = "/tmp/" + token
        os.makedirs(self.tmp_dir, exist_ok=True)

    def download(self, sources):
        for source in sources:
            for file in source['files']:
                source_path = None
                if isinstance(file, dict):
                    source_path = file['url']
                if isinstance(file, str):
                    source_path = file

                if source_path:
                    handler = FileHandlerFactory().create_for_url(url=source_path)

                    creds = source.get('credentials', None)
                    if creds:
                        handler.set_credentials(creds)

                    log.info("Downloading {} into {}".format(source_path, self.tmp_dir))
                    handler.download(src_path=source_path, tgt_path=self.tmp_dir)

        return 1
