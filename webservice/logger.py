import logging
import google.cloud.logging
from google.cloud.logging.handlers import CloudLoggingHandler

client = google.cloud.logging.Client()
handler = CloudLoggingHandler(client, name="snatcha")
google.cloud.logging.handlers.setup_logging(handler)

class SnatchaLogger:
    def __init__(self, component):
        # Instantiates a client

        self.log = logging.getLogger('snatcha.{}'.format(component))
        self.log.addHandler(handler)

    @property
    def logger(self):
        return self.log
