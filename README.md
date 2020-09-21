# snatcha
A remote file grabber

## Architecture
Snatcha contains 2 components:
- An HTTP cloud function, which is the web service that the users interact with
- A virtual machine hosting a Flask web service, which is doing the heavy lifting of transferring files

## Setup

### Virtual Machine

After creating a new virtual machine, run the setup.sh script from the `instance_setup` folder to configure it and start the service.

#### Auto-start

You also need to allow the service to start automatically at startup. The easiest way to do that is to 
add custom metadata to the instance.

Create a custom metadata called `startup-script` containing:
```
#! /bin/bash
/usr/bin/snatcha/instance_setup/auto-off.sh &
python3 /usr/bin/snatcha/webservice/app.py &
```

### Cloud Function

```
gcloud functions deploy snatcha --region=europe-west1 --entry-point=main --runtime python37 \
        --trigger-http --allow-unauthenticated \
        --set-env-vars INSTANCE_ID_=8400732780731087393,PROJECT_NAME_=bitmovin-solutions,ZONE_=europe-west-1
```
You can change the function and and region as required.
You also need to set the environment variables according to your configuration, and in particular set the INSTANCE_ID_ to the identifier of the VM created in the previous step

 