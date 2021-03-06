import requests
import shutil
import sys
sys.path.append("..")

import os
import logging

log = logging.getLogger('snatcha.http')

class HttpFileHandler:

    def __init__(self):
        pass

    def get_filename(self, path):
        flname = os.path.basename(path)
        flname = flname.split('?', 1)[0]
        log.info("Filename will be {}".format(flname))
        return flname

    def download(self, src_path, tgt_path):
        tgt_file_path = os.path.join(tgt_path, self.get_filename(src_path))

        log.info("Downloading file {} -> {}".format(src_path, tgt_file_path))

        with requests.get(src_path, stream=True) as r:
            if r.status_code == 200:
                with open(tgt_file_path, 'wb') as f:
                    shutil.copyfileobj(r.raw, f)
            else:
                raise RuntimeError("Unable to download HTTP {}: {}".format(src_path, r.reason))

        return tgt_file_path

    def parse_url(self, url):
        pass


class HttpFileHandlerBuilder:

    @classmethod
    def make(cls, **_ignored):
        return HttpFileHandler()
