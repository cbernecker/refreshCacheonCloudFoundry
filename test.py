### BLUEMIX
from flask import Flask, render_template, request, jsonify
import datetime
import requests
import os
import json

app = Flask(__name__)
CF_INSTANCE_INDEX = os.getenv("CF_INSTANCE_INDEX") if os.getenv("CF_INSTANCE_INDEX") else "LOCAL SYSTEM"
cache_file = {"MY_CACHE1" : "OBJECT1", "MY_CACHE2" : "OBJECT2"}
# On Bluemix, get the port number from the environment variable PORT
# When running this app on the local machine, default the port to 8000
port = int(os.getenv('PORT', 8000))

@app.route('/api/v1/current', methods=['POST','GET'])
def current():
    return jsonify({"Instance": CF_INSTANCE_INDEX,
                    "Cache Object" : cache_file})

@app.route('/api/v1/update', methods=['POST','GET'])
def update():
    cache_file['MY_CACHE3'] = request.json['MY_CACHE']
    return jsonify({"Instance": CF_INSTANCE_INDEX,
                    "Cache Object" : cache_file})

#invoked by @app.route('/api/v1/refresh', methods=['POST','GET'])
@app.route('/api/v1/refresh_all', methods=['POST','GET'])
def refresh_all():
    # Add your Function that Refresh the cache on one instacne
    cache_file['MY_CACHE3'] = request.json['MY_CACHE']
    return jsonify({'Refreshing': "Instance" })


@app.route('/api/v1/refresh', methods=['POST','GET'])
def refresh():
    print(str(request.json))
    instance = 0
    HTTP_STATUS = 200
    try:
        vcap = json.loads(os.getenv('VCAP_APPLICATION'))
        GUID = vcap['application_id']
        APPLICATION_URL = vcap['application_uris'][0]
        url = "https://" + APPLICATION_URL + "/api/v1/refresh_all"
        while HTTP_STATUS == 200:
            print("Refresh Instance: " + str(instance) + " on " + url)
            headers = {
                    'Content-Type': "application/json",
                    'X-CF-APP-INSTANCE': GUID + ":" + str(instance),
                    'cache-control': "no-cache",
                }
            r = requests.post(url, json=request.json, headers=headers)
            HTTP_STATUS = r.status_code
            instance = instance + 1
        return jsonify({'Refreshing': "Done", "Instances_Refreshed":instance-1})
    # For Local Development
    except TypeError as error:
        print(str(datetime.datetime.now()) + " WARNING: Seems to be the local development machine no VCAP_APPLICATION found")
        return jsonify({"WARNING" : "Seems to be the local development machine no VCAP_APPLICATION found"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=False, threaded=True)