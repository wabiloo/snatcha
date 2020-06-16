from flask import Flask, flash, render_template, request, redirect

import uuid

import requests

import json

from utils import payload

app = Flask(__name__)
app.secret_key = str(uuid.uuid4())

# Cloud function trigger
BASE_URL = "https://europe-west1-bitmovin-solutions.cloudfunctions.net/snatcha-dev-fabre"

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        # Get data from forms
        source_files = []
        for i in request.form:
            if i.startswith('new'):
                source_files.append(request.form[i])
        access_key = request.form['access']
        secret_key = request.form['secret']
        target_access_key = request.form['targetaccess']
        target_secret_key = request.form['targetsecret']
        output_bucket = request.form['bucket']
        output_path = request.form['bucketpath']

        # Construct payload
        headers = {
            'Content-Type': 'application/json',
        }

        # Check if any source input credentials exist.
        generate_payload = payload.generatePayload(
            source_files, output_bucket, output_path,
            target_access_key, target_secret_key
        )
        if len(access_key) == 0 and len(secret_key) == 0:
            data = generate_payload.no_input_credentials()
            print('PAYLOAD')
            print(data)
        else:
            data = generate_payload.input_credentials(access_key, secret_key)
            print('PAYLOAD')
            print(data)

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
    print(job_id)
    print(load_response)
    return render_template('process.html', job_id=job_id, data=load_response)

if __name__ == '__main__':
    # app.run(debug=True,
    #         host="0.0.0.0",
    #         port=80)
    app.run(debug=True)