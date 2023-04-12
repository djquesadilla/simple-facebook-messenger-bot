from flask import Flask, request
import requests

import os

app = Flask(__name__)

PAGE_ACCESS_TOKEN = os.environ.get('PAGE_ACCESS_TOKEN')
LATEST_API_VERSION="v16.0"
VERIFY_TOKEN = "myverifytoken"
API = "https://graph.facebook.com/" + LATEST_API_VERSION + "/me/messages?access_token="+PAGE_ACCESS_TOKEN

@app.route("/", methods=['GET'])
def fbverify():
    print("Hello world")
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token")==VERIFY_TOKEN:
            return "Verification token missmatch", 403
        return request.args['hub.challenge'], 200
    return "Hello world", 200

@app.route("/", methods=['POST'])
def fbwebhook():
    data = request.get_json()
    print(data)
    try:
        # Read messages from facebook messanger.
        message = data['entry'][0]['messaging'][0]['message']
        sender_id = data['entry'][0]['messaging'][0]['sender']['id']
        if message['text'] == "hi":
            request_body = {
                "recipient": {
                    "id": sender_id
                },
                "message": {
                    "text": "hello, world!"
                }
            }
            response = requests.post(API, json=request_body).json()
            print(response)
            return response
        else:
            request_body = {
                "recipient": {
                    "id": sender_id
                },
                "message": {
                    "text": "I don't understand"
                }
            }
            response = requests.post(API, json=request_body).json()
            print(response)
            return response
    except:
        request_body = {
                "recipient": {
                    "id": sender_id
                },
                "message": {
                    "text": "I don't understand"
                }
            }
        response = requests.post(API, json=request_body).json()
        print(response)
        return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)