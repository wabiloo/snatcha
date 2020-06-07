from flask import Flask, request
from uuid import uuid4
import logging
import json

from threading import Thread
from process import process_job

from google.cloud import firestore

from logger import SnatchaLogger

logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.CRITICAL)
log = SnatchaLogger('flask').logger

app = Flask("snatcha")
app.logger.setLevel(logging.DEBUG)

db = firestore.Client()

@app.route('/')
def hello():
    return "Hello World!"


""" Transfer route when job already created in firestore """
@app.route('/transfer-job', methods=['POST'])
def transfer_job():
    data = request.json
    log.debug("REQUEST: " + json.dumps(data, indent=2))
    print("REQUEST", data)

    job_id = data['job_id']

    doc_ref = db.collection("snatcha_jobs").document(job_id)
    job = doc_ref.get()

    if job.exists:
        data = job.to_dict()
        return start_process_thread(job_id, data, doc_ref)
    else:
        return dict(status='ERROR', message="No job with id {} exists in the database".format(job_id))


""" Direct transfer route (straight to the VM, without using job already in firestore """
@app.route('/transfer', methods=['POST'])
def transfer():
    data = request.json
    log.debug("REQUEST: " + json.dumps(data, indent=2))
    print("REQUEST", data)

    job_id = "direct_" + str(uuid4())
    log.info("JOB ID: " + job_id)

    job = dict(payload=data)

    doc_ref = db.collection("snatcha_jobs").document(job_id)
    doc_ref.set(job)

    return start_process_thread(job_id, job, doc_ref)


def start_process_thread(job_id, data, doc_ref):
    print("JOB", data)
    print("JOB ID", job_id)
    # threading allows us to return a response quickly, and not wait for the job to be processed
    thread = Thread(target=process_job,
                    kwargs={
                        'token': job_id,
                        'job': data
                    })

    doc_ref.update(dict(status="STARTING"))
    thread.start()
    return dict(job_id=job_id, status='STARTED')


if __name__ == '__main__':
    app.run(debug=True,
            host="0.0.0.0",
            port=80)
