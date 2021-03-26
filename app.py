# -*- coding: utf-8 -*-

from flask import Flask, request
from linebot.models import *
from linebot import *
import json
import requests

app = Flask(__name__)

line_bot_api = LineBotApi('Zwx/+Omyn03+o6EDoEx1WnxFRk5sFNhpGaAX335P8mg9eXotr0rGIM1kMD9jUf3Zd1rQvLf4nWChErouJ4ELXtK+4edCz/R9HFlTFJxuPkQA/DhBWi6hw5BEKh1hPGfSHUhHBS82mom3unpkk0OXvwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('6ce76d73dc225dc3e93e6f7c212cb94f')

@app.route("/callback", methods=['POST'])

def callback():

    #body = request.get_data(as_text=True)
    #print(body)
    req = request.get_json(silent=True, force=True)
    intent = req["queryResult"]["intent"]["displayName"]
    text = req['originalDetectIntentRequest']['payload']['data']['message']['text']
    reply_token = req['originalDetectIntentRequest']['payload']['data']['replyToken']
    id = req['originalDetectIntentRequest']['payload']['data']['source']['userId']

    profile = line_bot_api.get_profile(id, 10)

    disname = profile.display_name

    print('id = ' + id)
    print('name = ' + disname)
    print('text = ' + text)
    print('intent = ' + intent)
    print('reply_token = ' + reply_token)
    reply(intent, text, reply_token, id, disname)

    return 'OK'

def reply(intent,text,reply_token,id,disname):
    if intent == 'intent2':
        text_message = TextSendMessage(text='ทดสอบสำเร็จ')
        line_bot_api.reply_message(reply_token,text_message)
    elif intent == 'covid 19':
        data = requests.get('https://covid19.th-stat.com/api/open/today')
        json_data = json.loads(data.text)
        Confirmed = format(json_data['Confirmed'], ',d')  # ติดเชื้อสะสม
        Recovered = format(json_data['Recovered'], ',d')  # หายแล้ว
        Hospitalized = format(json_data['Hospitalized'], ',d')  # รักษาอยู่ใน รพ.
        Deaths = format(json_data['Deaths'], ',d')  # เสียชีวิต
        NewConfirmed = format(json_data['NewConfirmed'], ',d')  # บวกเพิ่ม
        text_message = TextSendMessage(
            text='ติดเชื้อสะสม = {} คน(+เพิ่ม {})\nหายแล้ว = {} คน\nรักษาอยู่ใน รพ. = {} คน\nเสียชีวิต = {} คน'.format(
                Confirmed, NewConfirmed, Recovered, Hospitalized, Deaths))

        line_bot_api.reply_message(reply_token, text_message)


if __name__ == "__main__":
    app.run()