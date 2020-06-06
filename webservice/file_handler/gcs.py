import sys

sys.path.append("..")

import os
import logging
from boto3.session import Session
import botocore
import boto3

logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('s3transfer').setLevel(logging.CRITICAL)


class GcsFileHandler:

    def __init__(self):
        self.session = boto3.Session()
        self.gsresource = self.session.resource('s3')

    def get_filename(self, path):
        return os.path.basename(path)

    def copy(self, src_path, tgt_path):
        return self.download(src_path, tgt_path)

    def download(self, src_path, tgt_path):
        try:
            (bucket, key) = self.parse_url(src_path)
            filename = self.get_filename(src_path)
            tgt_file_path = os.path.join(tgt_path, filename)

            self.gsresource.Bucket(bucket).download_file(key, tgt_file_path)
            return tgt_file_path
        except botocore.exceptions.ClientError as e:
            raise RuntimeError(e.args[0])


    def upload(self, src_path, tgt_path, bucket):
        try:
            filename = self.get_filename(src_path)
            tgt_file_path = os.path.join(tgt_path, filename)

            self.gsresource.Bucket(bucket).upload_file(src_path, tgt_file_path)
        except boto3.exceptions.S3UploadFailedError as e:
            raise RuntimeError(e.args[0])

    def parse_url(self, url):
        url = url.replace("gs://", "")

        bucket = url.split('/')[0]
        prefix = url.replace(bucket + "/", "")

        return bucket, prefix

    def _build_url(self, bucket, key):
        return "gs://{}/{}".format(bucket, key)

    def set_credentials(self, credentials):
        self.session = Session(aws_access_key_id=credentials['access_key'],
                               aws_secret_access_key=credentials['secret_key'])
        self.session.events.unregister('before-parameter-build.s3.ListObjects',
                                       botocore.handlers.set_list_objects_encoding_type_url)
        self.gsresource = self.session.resource('s3', endpoint_url='https://storage.googleapis.com',
                                                config=botocore.client.Config(signature_version='s3v4'))


class GcsFileHandlerBuilder:

    @classmethod
    def make(cls, **_ignored):
        return GcsFileHandler()
