# -*- coding: utf-8 -*-
import json
import pprint
import datetime


import requests
from flask import Flask, request, make_response, jsonify

# Bot User OAuth Token ( Application --> OAuth & Permissions )         
token  = '.....'
#slack = Slacker(token)

app = Flask(__name__)

def get_answer():
    return "안녕하세요."



# 이벤트 핸들하는 함수
def event_handler(event_type, slack_event):
    if event_type == "app_mention":
        channel = slack_event["event"]["channel"]

        text = get_answer() 
        response = requests.post("https://slack.com/api/chat.postMessage",
            headers={"Authorization": "Bearer "+token},
            data={"channel": channel,"text": text}
        )
        print(response)    
        return make_response("앱 멘션 메시지가 보내졌습니다.", 200, )
    elif event_type == "message":
        channel  = slack_event["event"]["channel"]
        rcv_text = slack_event["event"]["text"]

        print("channel's Name : " + channel)
        now = datetime.datetime.now()
        nowDatetime = now.strftime('%Y-%m-%d %H:%M:%S') ## 2015-04-19 12:11:32
        text = nowDatetime + " : received="+ rcv_text
        print(text) 
        
        if rcv_text == "hahaha":
            response = requests.post("https://slack.com/api/chat.postMessage",
                headers={"Authorization": "Bearer "+token},
                data={"channel": channel,"text": text}
            )
            print(response)    
            return make_response("앱 멘션 메시지가 보내졌습니다.", 200, )
    message = "[%s] 이벤트 핸들러를 찾을 수 없습니다." % event_type
    return make_response(message, 200, {"X-Slack-No-Retry": 1})



@app.route("/slack", methods=["GET", "POST"])
def hears():
    slack_event = json.loads(request.data)
    if "challenge" in slack_event:
        return make_response(slack_event["challenge"], 200, {"content_type": "application/json"})

    if "event" in slack_event:
        event_type = slack_event["event"]["type"]
        return event_handler(event_type, slack_event)
    return make_response("슬랙 요청에 이벤트가 없습니다.", 404, {"X-Slack-No-Retry": 1})

    
if __name__ == '__main__':
    app.run('0.0.0.0', port=8080)

