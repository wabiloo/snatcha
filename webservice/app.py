from flask import Flask, request
from uuid import uuid4
import logging
import json

from threading import Thread
from process import process_job

from google.cloud import firestore

logging.getLogger('googleapicliet.discovery_cache').setLevel(logging.CRITICAL)

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
    print("REQUEST", data)

    job_id = data['job_id']

    doc_ref = db.collection("snatcha_jobs").document(job_id)
    job = doc_ref.get()

    if job.exists:
        data = job.to_dict()
        print("JOB", data)
        # threading allows us to return a response quickly, and not wait for the job to be processed
        thread = Thread(target=process_job,
                        kwargs={
                            'token': job_id,
                            'job': data
                        })

        doc_ref.update(dict(status="STARTING"))
        thread.start()

        return dict(job_id=job_id, status='STARTED')
    else:
        return dict(status='ERROR', message="No job with id {} exists in the database".format(job_id))


if __name__ == '__main__':
    app.run(debug=True,
            host="0.0.0.0",
            port=80)
