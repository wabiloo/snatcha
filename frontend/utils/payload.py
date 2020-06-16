

class generatePayload:
    """
    Returns a payload with the required keys
    """
    def __init__(self, source_files, output_bucket, output_path,
        target_access_key, target_secret_key):
        self.source_files = source_files
        self.output_bucket = output_bucket
        self.output_path = output_path
        self.target_access_key = target_access_key
        self.target_secret_key = target_secret_key
    

    def no_input_credentials(self):
        payload = {
                "sources": [
                    {
                        "files": self.source_files,
                    }
                ],
                "targets": [
                    {
                        "provider": "s3",
                        "bucket": self.output_bucket,
                        "credentials": {
                            "access_key": self.target_access_key,
                            "secret_key": self.target_secret_key
                        },
                        "path": self.output_path 
                    }
                ]
            }
        return payload

    def input_credentials(self, access_key, secret_key):
        payload = {
                "sources": [
                    {
                        "files": self.source_files,
                        "credentials": {
                                "access_key": access_key,
                                "secret_key": secret_key
                            },
                    }
                ],
                "targets": [
                    {
                        "provider": "s3",
                        "bucket": self.output_bucket,
                        "credentials": {
                            "access_key": self.target_access_key,
                            "secret_key": self.target_secret_key
                        },
                        "path": self.output_path 
                    }
                ]
            }
        return payload