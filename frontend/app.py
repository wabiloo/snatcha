from flask import Flask, render_template, request, redirect

import uuid

import requests

import json

app = Flask(__name__)
app.secret_key = str(uuid.uuid4())

# Cloud function trigger
BASE_URL = "https://europe-west1-bitmovin-solutions.cloudfunctions.net/snatcha-dev-fabre"

@app.route('/', methods=["POST", 'GET'])
def index():
    if request.method == "POST":
        # Get data from forms
        source_files = []
        for i in request.form:
            if i.startswith('new'):
                source_files.append(request.form[i])
        access_key = request.form['access']
        secret_key = request.form['secret']
        output_bucket = request.form['bucket']
        output_path = request.form['bucketpath']

        # Construct payload
        headers = {
            'Content-Type': 'application/json',
        }

        data = {
                "sources": [
                    {
                        "files": source_files,
                        "credentials": {
                            "access_key": access_key,
                            "secret_key": secret_key 
                        }
                    }
                ],
                "targets": [
                    {
                        "provider": "s3",
                        "bucket": output_bucket,
                        "credentials": {
                            "access_key": "AKIAIU6N2FVXCRB64HDQ",
                            "secret_key": "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"
                        },
                        "path": output_path 
                    }
                ]
            }

        # POST
        response = requests.post(BASE_URL + '/transfer', headers=headers, data=json.dumps(data))
        load_response = json.loads(response.text)
        print("CLOUD FUNCTION RESPONSE")
        print(load_response)
        return redirect('/process/' + load_response["job_id"])
    return render_template('index.html')

@app.route('/process/<job_id>', methods=['POST', 'GET'])
def process(job_id):
    response = requests.post(BASE_URL + '/status/' + job_id)
    load_response = json.loads(response.text)
    print(load_response)
    return render_template('process.html', job_id=job_id, data=load_response)

if __name__ == '__main__':
    app.run(debug=True)
