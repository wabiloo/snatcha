from flask import Flask, request
from uuid import uuid4
import logging
import json

from threading import Thread

from process import process_payload

app = Flask("snatcha")
app.logger.setLevel(logging.DEBUG)


@app.route('/')
def hello():
    return "Hello World!"


@app.route('/transfer', methods=['POST'])
def transfer():
    data = request.json
    logging.debug(json.dumps(data, indent=2))

    token = str(uuid4())

    thread = Thread(target=process_payload,
                    kwargs={
                        'token': token,
                        'payload': data
                    })
    thread.start()

    return {'id': token}


if __name__ == '__main__':
    app.run(debug=True,
            host="0.0.0.0",
            port=80)
