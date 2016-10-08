#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = processRequest(req)

    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") != "pullData":
        return {}
    baseurl = "https://jsonplaceholder.typicode.com/"
    yql_query = makeYqlQuery(req)
    if yql_query is None:
        return {}
    yql_url = baseurl + yql_query
    result = urllib.urlopen(yql_url).read()
    data = json.loads(result)
    res = makeWebhookResult(data)
    return res


def makeYqlQuery(req):
    entryNum = req.get("result").get("parameters").get("entryNum")
    atype = req.get("result").get("parameters").get("type")
    if type is None:
        return None

    return atype + "/" + entryNum


def makeWebhookResult(data):
    albumId = data.get('albumId')
    if title is None:
        return {}
    title = data.get('title')
    if title is None:
        return {}
    # print(json.dumps(item, indent=4))

    speech = "The albumId is " + albumId + " and it has the title " + title

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "MH8-Hackbot"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=False, port=port, host='0.0.0.0')
