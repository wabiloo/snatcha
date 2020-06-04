import logging
import os

from file_handler import FileHandlerFactory, LocalFileHandler

log = logging.getLogger('snatcha.upload')

class UploadHelper:
    def __init__(self, token):
        self.token = token
        self.tmp_dir = "/tmp/" + token

    def upload(self, destinations):
        files = LocalFileHandler().find_matching_files(local_root=self.tmp_dir,
                                                       path="*")

        for destination in destinations:
            handler = FileHandlerFactory().create_for_provider(destination['provider'])

            for file in files:
                creds = destination.get('credentials', None)
                if creds:
                    handler.set_credentials(creds)

                tgt_path = destination['path']
                log.info("Uploading {} -> {}".format(file, tgt_path))
                handler.upload(src_path=file, tgt_path=tgt_path)
