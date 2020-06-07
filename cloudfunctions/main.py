import datetime
import json
import os
import requests
import time
import uuid
import logging

import googleapiclient.discovery
from google.cloud import firestore

import fastjsonschema

from flask import jsonify

logging.getLogger('googleapiclient.discovery_cache').setLevel(logging.CRITICAL)

# Get VM ID
INSTANCE_ID = os.environ.get('INSTANCE_ID')
INSTANCE_ZONE = os.environ.get('INSTANCE_ZONE')
PROJECT_NAME = os.environ.get('GCP_PROJECT')

db = firestore.Client()

def main(request):
    print("PATH", request.path)
    print("QUERY", request.query_string)
    if request.path.startswith("/transfer"):
        return do_transfer(request)
    if request.path.startswith("/status"):
        return get_status(request)

    else:
        return "Invalid path"

def get_status(request):
    print("Handling status request")
    job_id = request.path.replace("/status/", "")
    print("JOB ID", job_id  )

    doc_ref = db.collection('snatcha_jobs').document(job_id)
    doc = doc_ref.get()
    if doc.exists:

        safe_result = sanitize(doc.to_dict())
        return jsonify(safe_result)
    else:
        return "Invalid job_id {}".format(job_id)


def do_transfer(request):
    print("Handling transfer request")
    payload = request.get_json(silent=True)
    print("PAYLOAD", payload)

    job_id = str(uuid.uuid4())
    print("JOB ID", job_id)
    doc_ref = db.collection('snatcha_jobs').document(job_id)
    doc_ref.set(dict(payload=payload,
                     status="PENDING",
                     created_at=datetime.datetime.now().isoformat()))

    # Validate job against schema
    with open("schema_transfer.json") as schema_file:
        schema = json.load(schema_file)
        try:
            fastjsonschema.validate(schema, payload)
        except fastjsonschema.exceptions.JsonSchemaException:
            doc_ref.update(dict(status="INVALID_PAYLOAD",
                                messages=["Invalid payload submitted"]))
            return jsonify(dict(job_id=job_id,
                                status="INVALID_PAYLOAD"))
        except Exception as e:
            doc_ref.update(dict(status="ERROR_OTHER",
                                messages=["Error in validating payload with schema: {}".format(str(e))]))
            return jsonify(dict(job_id=job_id,
                                status="ERROR"))

    # Init gcp client
    instance_manager = InstanceManager(
        project_name=PROJECT_NAME,
        zone=INSTANCE_ZONE,
        instance_id=INSTANCE_ID
    )

    response_body = dict(job_id=job_id)
    while True:
        # Check instance status every x seconds
        time.sleep(1)
        instance_status = instance_manager.status()
        if instance_status == 'RUNNING':
            # ====== POST REQUEST TO SNATCHA VM ======
            BASE_URL = 'http://' + instance_manager.external_ip()
            print(BASE_URL)
            headers = {
                'Content-Type': 'application/json',
            }
            # Pass this endpoints request data to snatcha VM
            # Format request body
            _data = dict(job_id=job_id)
            data = f"""{_data}""".replace('\'', '"')
            # POST to snatcha VM
            response = requests.post(
                BASE_URL + '/transfer-job',
                headers=headers,
                data=json.dumps(_data)
            )
            print('The instance is running. \nStatus: ' + instance_status)
            print(response.text)
            response_body = response.json()
            break
        elif instance_status == 'PROVISIONING':
            print('The instance is booting up. \nStatus: ' + instance_status)
            doc_ref.update(dict(status=instance_status))
            continue
        elif instance_status == 'STAGING':
            print('The instance is booting up. \nStatus: ' + instance_status)
            doc_ref.update(dict(status=instance_status))
            continue
        elif instance_status == 'REPAIRING':
            print('The instance has encounted an issue. \nStatus: ' + instance_status)
            doc_ref.update(dict(status='ERROR',
                                messages=["The instance has encountered an issue and in REPAIRING status"]))
            break
        else:
            print('INSTANCE STATUS: ' + instance_status)
            start_instance = instance_manager.start()
            _to_return = start_instance
            continue

    return jsonify(response_body)

def sanitize(doc):
    pld = doc['payload']

    for direction in ['sources', 'targets']:
        if direction in pld:
            for part in pld[direction]:
                if 'credentials' in part:
                    creds = part['credentials']
                    for field in ['secret_key', 'password']:
                        if field in creds:
                            creds[field] = "***" + creds[field][-4:]
    return doc


class InstanceManager:
    """
    Management of GCP instances
    """
    def __init__(self, project_name, zone, instance_id):
        self.project_name = project_name
        self.zone = zone
        self.instance_id = instance_id
        # Init gcp client
        self.compute = googleapiclient.discovery.build('compute', 'v1', cache_discovery=False)

    def start(self):
        """
        Start GCP instance
        """
        call_start = self.compute.instances().start( project=self.project_name,
            zone=self.zone, instance=self.instance_id).execute()
        print(call_start)
        return call_start

    def status(self):
        """
        Get the current state of the instance
        """
        get_instance = self.compute.instances().get( project = self.project_name,
            zone=self.zone,instance = self.instance_id).execute()
        print(get_instance)
        return get_instance['status']

    def external_ip(self):
        """
        Get the ip of the snatcha server
        """
        get_instance = self.compute.instances().get( project = self.project_name,
            zone=self.zone,instance = self.instance_id).execute()
        print(get_instance)
        for network_interfaces in get_instance['networkInterfaces']:
            for acccess_configs in network_interfaces['accessConfigs']:
                ip = acccess_configs['natIP']
        return ip

