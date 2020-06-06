import os
import requests
import time
import uuid

import googleapiclient.discovery
from google.cloud import firestore
from google.cloud import error_reporting

from flask import jsonify

# Get VM ID
INSTANCE_ID = os.environ.get('INSTANCE_ID')
INSTANCE_ZONE = os.environ.get('INSTANCE_ZONE')
PROJECT_NAME = os.environ.get('GCP_PROJECT')

db = firestore.Client()

def main(request):
    payload = request.get_json(silent=True)
    print(payload)

    job_id = str(uuid.uuid4())
    doc_ref = db.collection('snatcha_jobs').document(job_id)
    doc_ref.set(dict(payload=payload,
                     status="PENDING"))

    # Init gcp client
    instance_manager = InstanceManager(
        project_name=PROJECT_NAME,
        zone=INSTANCE_ZONE,
        instance_id=INSTANCE_ID
    )

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
            _data = payload
            data = f"""{_data}""".replace('\'', '"')
            # POST to snatcha VM
            response = requests.post(
                BASE_URL + '/transfer',
                headers=headers,
                data=jsonify(job_id=job_id)
            )
            print('The instance is running. \nStatus: ' + instance_status)
            print(response.text)
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

    return job_id


class InstanceManager:
    """
    Management of GCP instances
    """
    def __init__(self, project_name, zone, instance_id):
        self.project_name = project_name
        self.zone = zone
        self.instance_id = instance_id
        # Init gcp client
        self.compute = googleapiclient.discovery.build('compute', 'v1')

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

