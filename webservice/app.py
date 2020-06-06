from flask import Flask, request
from uuid import uuid4
import logging
import json

from threading import Thread
from process import process_payload

from google.cloud import firestore

app = Flask("snatcha")
app.logger.setLevel(logging.DEBUG)

db = firestore.Client()

@app.route('/')
def hello():
    return "Hello World!"


@app.route('/transfer', methods=['POST'])
def transfer():
    data = request.json
    logging.debug(json.dumps(data, indent=2))

    job_id = data['job_id']

    doc_ref = db.collection("snatcha_jobs").document(job_id)
    job = doc_ref.get()

    if job.exists():
        thread = Thread(target=process_payload,
                        kwargs={
                            'token': job_id,
                            'payload': data
                        })
    thread.start()

    return dict(id=job_id, status='STARTED')


if __name__ == '__main__':
    app.run(debug=True,
            host="0.0.0.0",
            port=80)
