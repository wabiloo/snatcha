from .local import LocalFileHandlerBuilder
from .s3 import S3FileHandlerBuilder
from .http import HttpFileHandlerBuilder
from .gcs import GcsFileHandlerBuilder

class FileHandlerFactory(object):
    def __init__(self):
        self._builders = {
            'local': LocalFileHandlerBuilder,
            's3': S3FileHandlerBuilder,
            'http': HttpFileHandlerBuilder,
            'gcs': GcsFileHandlerBuilder
        }

    def create_for_url(self, url, **kwargs):
        key = None
        if url.startswith("s3://"):
            key = 's3'
        elif url.startswith("gs://"):
            key = 'gcs'
        elif url.startswith("http://") or url.startswith("https://"):
            key = 'http'
        else:
            key = 'local'

        builder = self._builders.get(key)
        if not builder:
            raise ValueError(key)
        return builder.make(**kwargs)

    def create_for_provider(self, provider, **kwargs):
        builder = self._builders.get(provider)
        if not builder:
            raise ValueError(provider)
        return builder.make(**kwargs)


