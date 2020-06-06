# snatcha
A remote file grabber

## Architecture
Snatcha contains 2 components:
- An HTTP cloud function, which is the web service that the users interact with
- A virtual machine hosting a Flask web service, which is doing the heavy lifting of transferring files

## Setup

### Virtual Machine

After creating a new virtual machine, run the setup.sh script to configure it and start the service.

#### Auto-start

You also need to allow the service to start automatically at startup. The easiest way to do that is to modify the `/etc/rc.local` file
and add the call to start the flask app into it.

```
#!/bin/sh -e
python3 /usr/bin/snatcha/webservice/app.py &
exit 0
```

Make your /etc/rc.local executable in case it is not already executable by

```
sudo chown root /etc/rc.local
sudo chmod 755 /etc/rc.local
```

Check everything works fine by executing
```
sudo /etc/rc.local start
```

### Cloud Function

```
gcloud functions deploy snatcha --region=europe-west1 --entry-point=main --runtime python37 \
        --trigger-http --allow-unauthenticated \
        --set-env-vars INSTANCE_ID_=8400732780731087393,PROJECT_NAME_=bitmovin-solutions,ZONE_=europe-west-1
```
You can change the function and and region as required.
You also need to set the environment variables according to your configuration, and in particular set the INSTANCE_ID_ to the identifier of the VM created in the previous step

 