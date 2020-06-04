import sys
sys.path.append("..")

from pathlib import Path
import os
import shutil
import logging

log = logging.getLogger('snatcha.local')

class LocalFileHandler:

    def __init__(self):
        self.is_remote = False

    def get_filename(self, path):
        return os.path.basename(path)

    def find_matching_files(self, path, local_root, filter="", **kwargs):
        output_files = list(Path(local_root).glob(path))

        files = []
        for output_file in output_files:
            # TODO - Implement filter

            files.append(output_file)

        return files

    def copy(self, src_path, tgt_path):
        return shutil.copy2(src_path, tgt_path)

    def upload(self, src_path, tgt_path):
        log.debug("Copying {} to {}".format(src_path, tgt_path))
        return self.copy(src_path, tgt_path)

class LocalFileHandlerBuilder:

    @classmethod
    def make(self, **_ignored):
        return LocalFileHandler()
