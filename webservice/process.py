import logging
import shutil

from download import DownloadHelper
from upload import UploadHelper

def process_payload(token, payload):
    downloader = DownloadHelper(token=token)
    downloader.download(payload['sources'])

    uploader = UploadHelper(token=token)
    uploader.upload(payload['targets'])

    clean_local_files(token=token)


def clean_local_files(token):
    log = logging.getLogger('snatcha.clean')
    tmp_dir = "/tmp/" + token

    log.debug("Deleting temporary folder {}".format(tmp_dir))
    shutil.rmtree(tmp_dir, ignore_errors=True)

