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
    print(intent)
    if intent == 'intent2':
        text_message = TextSendMessage(text='ทดสอบสำเร็จ')
    elif intent == 'covid 19':
        data = requests.get('https://covid19.th-stat.com/api/open/today')
        json_data = json.loads(data.text)
        #print(json_data)
        Confirmed = format(json_data['Confirmed'], ',d')  # ติดเชื้อสะสม
        Recovered = format(json_data['Recovered'], ',d')  # หายแล้ว
        Hospitalized = format(json_data['Hospitalized'], ',d')  # รักษาอยู่ใน รพ.
        Deaths = format(json_data['Deaths'], ',d')  # เสียชีวิต
        NewConfirmed = format(json_data['NewConfirmed'], ',d')  # บวกเพิ่ม
        UpdateDate = json_data['UpdateDate']
        toDay = UpdateDate.split(' ')[0]
        #print(UpdateDate)
        text_message = TextSendMessage(
            text='รายงานผู้ติด COVID-19 ในประเทศไทยประจำวันที่ {}\n\nติดเชื้อสะสม = {} คน(+เพิ่ม {})\nหายแล้ว = {} คน\nรักษาอยู่ใน รพ. = {} คน\nเสียชีวิต = {} คน\n\n**Updated : {}'.format(
                toDay, Confirmed, NewConfirmed, Recovered, Hospitalized, Deaths, UpdateDate))
    elif intent == 'company_addr':
        compgrp_id = ''
        text = text.upper()

        if text.find("TIC") >= 0 :
            compgrp_id = 'TIC'
        elif text.find("STC") >= 0 :
            compgrp_id = 'STC'
        elif text.find("TNH") >= 0 :
            compgrp_id = 'TNH'
        elif text.find("TNH") >= 0 :
            compgrp_id = 'TNH'
        elif text.find("DRD") >= 0:
            compgrp_id = 'DRD'
        elif text.find("SP") >= 0:
            compgrp_id = 'SP'
        elif text.find("PCM") >= 0:
            compgrp_id = 'PCM'
        elif text.find("PYA") >= 0  or text.find("โป่งแยง") >= 0:
            compgrp_id = 'PYA'
        elif text.find("DTC") >= 0  or text.find("ดอยสะเก็ด") >= 0:
            compgrp_id = 'DTC'
        elif text.find("MANSION") >= 0  or text.find("ซอย 40") >= 0 or text.find("ซอย40") >= 0 or text.find("ซ.40") >= 0 or text.find("ซ. 40") >= 0:
            compgrp_id = 'MANSION'
        elif text.find("โรงน้ำ") >= 0  or text.find("BWP") >= 0 :
            compgrp_id = 'BWP'

        path = "address/"
        addr = ""
        file1 = open(path + compgrp_id+".txt", encoding="utf8")
        while True:
            # Get next line from file
            line = file1.readline()
            if not line:
                break

            addr += line.strip()+"\n"

        file1.close()
        text_message = TextSendMessage(text=addr)

    elif intent == 'holiday':
        holiday = ""
        path = "hr/"
        file1 = open(path + "holiday.txt", encoding="utf8")
        while True:
            # Get next line from file
            line = file1.readline()
            if not line:
                break

            holiday += line.strip()+"\n"

        file1.close()
        text_message = TextSendMessage(text=holiday)

    elif intent == 'ext_number':
        dep_id = ''
        text = text.upper()
        if text.find("ไอที") >= 0 or text.find("IT") >= 0 :
            dep_id = 'IT'
        elif text.find("ตปท") >= 0 or text.find("ต่างประเทศ") >= 0 or text.find("FOREIGN") >= 0:
            dep_id = 'FOREIGN'
        elif text.find("บัญชี") >= 0 or text.find("ACCOUNT") >= 0 :
            dep_id = 'ACCOUNT'
        elif text.find("สินค้า") >= 0 or text.find("สินค้าขาย") >= 0 or text.find("PRODUCT") >= 0 :
            dep_id = 'PRODUCT'
        elif text.find("ขาย") >= 0 or text.find("ตลาด") >= 0 or text.find("การตลาด") >= 0 or text.find("SALES") >= 0 :
            dep_id = 'SALES'
        elif text.find("การเงิน") >= 0 or text.find("FINANCE") >= 0 :
            dep_id = 'FINANCE'
        elif text.find("แลป") >= 0 or text.find("เทคนิค") >= 0 or text.find("LAB") >= 0:
            dep_id = 'LAB'
        elif text.find("ผลิต") >= 0 or text.find("PRODUCTION") >= 0:
            dep_id = 'PRODUCTION'
        elif text.find("คลัง") >= 0 or text.find("คลังสินค้า") >= 0 or text.find("GODOWN") >= 0:
            dep_id = 'GODOWN'
        elif text.find("จัดส่ง") >= 0 or text.find("LOGISTIC") >= 0:
            dep_id = 'LOGISTIC'
        elif text.find("HR") >= 0 or text.find("ธุรการ") >= 0 or text.find("บุคคล") >= 0:
            dep_id = 'HR'
        #extNumber = getExtNumber(dep_id)


        path = "ext_number/"

        print(path + dep_id+".txt")

        file1 = open(path + dep_id+".txt", encoding="utf8")
        file_as_list = file1.readlines()
        extNumber = ""
        for line in file_as_list:
            # Get next line from file
            #line = file1.readline()
            extNumber += line.strip()+"\n"
        file1.close()
        text_message = TextSendMessage(text=extNumber)

    line_bot_api.reply_message(reply_token, text_message)

if __name__ == "__main__":
    app.run()