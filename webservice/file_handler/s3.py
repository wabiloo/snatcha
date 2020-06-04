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

    def __init__(self, aws_profile):
        # Any clients created from this session will use credentials
        # from the [<aws_profile>] section of ~/.aws/credentials.

        self.aws_profile = aws_profile
        self.session = boto3.Session(profile_name=self.aws_profile)
        self.s3resource = self.session.resource('s3')
        self.s3client = self.session.client('s3')

    def get_filename(self, path):
        return os.path.basename(path)

    def copy(self, src_path, tgt_path):
        return self.download(src_path, tgt_path)

    def download(self, src_path, tgt_path):
        (bucket, key) = self.parse_url(src_path)
        self.s3resource.Bucket(bucket).download_file(key, tgt_path)
        return tgt_path

    def parse_url(self, url):
        url = url.replace("s3://","")

        bucket = url.split('/')[0]
        prefix = url.replace(bucket + "/", "")

        return bucket, prefix

    def _build_url(self, bucket, key):
        return "s3://{}/{}".format(bucket, key)


class S3FileHandlerBuilder:

    @classmethod
    def make(cls, aws_profile, **_ignored):
        return S3FileHandler(aws_profile)
