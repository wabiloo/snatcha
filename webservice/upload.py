import logging

from file_handler import FileHandlerFactory, LocalFileHandler

from logger import SnatchaLogger
log = SnatchaLogger('upload').logger

class UploadHelper:
    def __init__(self, token):
        self.token = token
        self.tmp_dir = "/tmp/" + token

    def upload(self, destinations):
        files = LocalFileHandler().find_matching_files(local_root=self.tmp_dir,
                                                       path="*")

        dest_files = []
        for destination in destinations:
            handler = FileHandlerFactory().create_for_provider(destination['provider'])

            for file in files:
                creds = destination.get('credentials', None)
                if creds:
                    handler.set_credentials(creds)

                params = {}
                if destination.get('bucket'):
                    params['bucket'] = destination.get('bucket')

                tgt_path = destination['path']
                log.info("Uploading {} to {}".format(file, tgt_path))

                tgt_file = handler.upload(src_path=str(file), tgt_path=tgt_path, **params)
                dest_files.append(tgt_file)

        return dest_files
