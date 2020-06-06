import requests

import time

import googleapiclient.discovery

from flask import jsonify

import os

# Get VM ID
INSTANCE_ID_ = os.environ.get('INSTANCE_ID_')
PROJECT_NAME_ = os.environ.get('PROJECT_NAME_')
ZONE_ = os.environ.get('ZONE_')

def main(request):
    print(request.get_json(silent=True))
    # Init gcp client
    manage_instance = manageInstance(
        project_name=PROJECT_NAME_,
        zone=ZONE_,
        instance_id=INSTANCE_ID_
    )
    while True:
        # Check instance status every x seconds
        time.sleep(1)
        instance_status = manage_instance.status()
        if instance_status == 'RUNNING':
            # ====== POST REQUEST TO SNATCHA VM ======
            BASE_URL = 'http://' + manage_instance.external_ip()
            print(BASE_URL)
            headers = {
                'Content-Type': 'application/json',
            }
            # Pass this endpoints request data to snatcha VM
            # Format request body
            _data = request.get_json(silent=True)
            data = f"""{_data}""".replace('\'', '"')
            # POST to snatcha VM
            response = requests.post(
                BASE_URL + '/transfer',
                headers=headers,
                data=data
            )
            print('The instance is running. \nStatus: ' + instance_status)
            print(response.text)
            break
        elif instance_status == 'PROVISIONING':
            print('The instance is booting up. \nStatus: ' + instance_status)
            continue
        elif instance_status == 'STAGING':
            print('The instance is booting up. \nStatus: ' + instance_status)
            continue
        elif instance_status == 'REPAIRING':
            print('The instance has encounted an issue. \nStatus: ' + instance_status)
            break
        else:
            print('INSTANCE STATUS: ' + instance_status)
            start_instance = manage_instance.start()
            _to_return = start_instance
            continue
    return response.text


class manageInstance:
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
