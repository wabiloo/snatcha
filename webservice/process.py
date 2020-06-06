import datetime
import logging
import shutil

from download import DownloadHelper
from upload import UploadHelper

from google.cloud import firestore

db = firestore.Client()

def process_job(token, job):
    job_spec = job['payload']

    doc_ref = db.collection("snatcha_jobs").document(token)
    doc_ref.update(dict(status='DOWNLOADING'))
    downloader = DownloadHelper(token=token)
    downloader.download(job_spec['sources'])

    doc_ref.update(dict(status='UPLOADING'))
    uploader = UploadHelper(token=token)
    results = uploader.upload(job_spec['targets'])

    clean_local_files(token=token)
    doc_ref.update(dict(status='COMPLETE',
                        results=results,
                        complete_at=datetime.datetime.now().isoformat()))


def clean_local_files(token):
    log = logging.getLogger('snatcha.clean')
    tmp_dir = "/tmp/" + token

    log.debug("Deleting temporary folder {}".format(tmp_dir))
    shutil.rmtree(tmp_dir, ignore_errors=True)

