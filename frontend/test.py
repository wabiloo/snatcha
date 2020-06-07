
import json

test = ['levi', 'one','two']


# data = """{{
#     "sources": [
#         {{
#             "files": {},
#             "credentials": {{
#                 "access_key": "AKIAIU6N2FVXCRB64HDQ",
#                 "secret_key": "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"
#             }}
#         }}
#     ],
#     "targets": [
#         {{
#             "provider": "s3",
#             "bucket": "bitmovin-api-eu-west1-ci",
#             "credentials": {{
#                 "access_key": "AKIAIU6N2FVXCRB64HDQ",
#                 "secret_key": "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"
#             }},
#             "path": "fabre/test1"
#         }}
#     ]
# }}
# """.format('test')

# print(data)

payload = {
    "sources": [
        {
            "files": [
                "https://previews.123rf.com/images/victoroancea/victoroancea1201/victoroancea120100059/12055848-tv-color-test-pattern-test-card-for-pal-and-ntsc.jpg",
                "https://www.denofgeek.com/wp-content/uploads/2018/04/the-flash-season-5-release-date-news-villain-story.jpg"
            ]
        },
        {
            "files": [
                "s3://bitmovin-api-eu-west1-ci/fabre/snatcha-source/plot_image.svg"
            ],
            "credentials": {
                "access_key": "AKIAIU6N2FVXCRB64HDQ",
                "secret_key": "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"
            }
        }
    ],
    "targets": [
        {
            "provider": "s3",
            "bucket": "bitmovin-api-eu-west1-ci",
            "credentials": {
                "access_key": "AKIAIU6N2FVXCRB64HDQ",
                "secret_key": "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"
            },
            "path": "fabre/test1"
        }
    ]
}