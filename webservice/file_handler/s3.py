import sys
sys.path.append("..")

import boto3
import re
import os
import logging

logging.getLogger('botocore').setLevel(logging.CRITICAL)
logging.getLogger('boto3').setLevel(logging.CRITICAL)
logging.getLogger('s3transfer').setLevel(logging.CRITICAL)

class S3FileHandler:

    def __init__(self):
        self.session = boto3.Session()
        self.s3resource = self.session.resource('s3')

    def get_filename(self, path):
        return os.path.basename(path)

    def copy(self, src_path, tgt_path):
        return self.download(src_path, tgt_path)

    def download(self, src_path, tgt_path):
        (bucket, key) = self.parse_url(src_path)
        filename = self.get_filename(src_path)
        tgt_file_path = os.path.join(tgt_path, filename)

        self.s3resource.Bucket(bucket).download_file(key, tgt_file_path)
        return tgt_file_path

    def upload(self, src_path, tgt_path, bucket):
        filename = self.get_filename(src_path)
        tgt_file_path = os.path.join(tgt_path, filename)

        self.s3resource.Bucket(bucket).upload_file(src_path, tgt_file_path)
        return self._build_url(bucket, tgt_file_path)

    def parse_url(self, url):
        url = url.replace("s3://","")

        bucket = url.split('/')[0]
        prefix = url.replace(bucket + "/", "")

        return bucket, prefix

    def _build_url(self, bucket, key):
        return "s3://{}/{}".format(bucket, key)

    def set_credentials(self, credentials):
        self.s3resource = self.session.resource(service_name='s3',
                                                aws_access_key_id=credentials['access_key'],
                                                aws_secret_access_key=credentials['secret_key'])


class S3FileHandlerBuilder:

    @classmethod
    def make(cls, **_ignored):
        return S3FileHandler()
