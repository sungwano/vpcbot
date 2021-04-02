# -*- coding: utf-8 -*-

from flask import Flask, request
from linebot.models import *
from linebot import *
import json
import requests
from mysql.connector import connection

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

    #print('id = ' + id)
    #print('name = ' + disname)
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
        print(json_data)
        Confirmed = format(json_data['Confirmed'], ',d')  # ติดเชื้อสะสม
        Recovered = format(json_data['Recovered'], ',d')  # หายแล้ว
        Hospitalized = format(json_data['Hospitalized'], ',d')  # รักษาอยู่ใน รพ.
        Deaths = format(json_data['Deaths'], ',d')  # เสียชีวิต
        NewConfirmed = format(json_data['NewConfirmed'], ',d')  # บวกเพิ่ม
        UpdateDate = json_data['UpdateDate']
        toDay = UpdateDate.split(' ')[0]
        print(UpdateDate)
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
        add = getAdd(compgrp_id)
        text_message = TextSendMessage(text=add)
    elif intent == 'ext_number':
        dep_id = ''
        text = text.upper()
        if text.find("ไอที") >= 0 or text.find("IT") >= 0 :
            dep_id = 'ไอที'
        elif text.find("ตปท") >= 0 or text.find("ต่างประเทศ") >= 0 or text.find("FOREIGN") >= 0:
            dep_id = 'ต่างประเทศ'
        elif text.find("บัญชี") >= 0 or text.find("ACCOUNT") >= 0 :
            dep_id = 'บัญชี'
        elif text.find("สินค้า") >= 0 or text.find("สินค้าขาย") >= 0 or text.find("PRODUCT") >= 0 :
            dep_id = 'สินค้าขาย'
        elif text.find("ขาย") >= 0 or text.find("ตลาด") >= 0 or text.find("การตลาด") >= 0 or text.find("SALES") >= 0 :
            dep_id = 'การตลาด'
        elif text.find("การเงิน") >= 0 or text.find("FINANCE") >= 0 :
            dep_id = 'การเงิน'
        elif text.find("แลป") >= 0 or text.find("เทคนิค") >= 0 or text.find("LAB") >= 0:
            dep_id = 'LAB'
        elif text.find("ผลิต") >= 0 or text.find("PRODUCTION") >= 0:
            dep_id = 'ผลิต'
        elif text.find("คลัง") >= 0 or text.find("คลังสินค้า") >= 0 or text.find("GODOWN") >= 0:
            dep_id = 'คลังสินค้า'
        elif text.find("จัดส่ง") >= 0 or text.find("LOGISTIC") >= 0:
            dep_id = 'จัดส่ง'
        elif text.find("HR") >= 0 or text.find("ธุรการ") >= 0 or text.find("บุคคล") >= 0:
            dep_id = 'ธุรการและการบุคคล'
        extNumber = getExtNumber(dep_id)
        text_message = TextSendMessage(text=extNumber)


    line_bot_api.reply_message(reply_token, text_message)

def getAdd(compgrpID):

    username = "vpcbot"
    passwd = "vpcbotvpcbot"
    host_name = "vpc-group.dyndns-office.com"
    db_name = "vpcbot"
    conn = connection.MySQLConnection(user=username, password=passwd,
                                          host=host_name, database=db_name)
    cursor = conn.cursor()

    #cursor.execute("SELECT compgrp_code,compgrp_id,compgrp_tname,address1,address2,CONCAT(district,' ',province,' ',postal_code), tax_id FROM vpcbot.company_add WHERE LENGTH(compgrp_id)>0 AND compgrp_id='" + compgrpID + "'  ORDER BY compgrp_code")
    cursor.execute("SELECT compgrp_code,compgrp_id,compgrp_tname,address1,address2,CONCAT(district,' ',province,' ',postal_code), tax_id FROM vpcbot.company_add WHERE LENGTH(compgrp_id)>0 AND compgrp_id='" + compgrpID + "'  ORDER BY compgrp_code")
    addr = ""
    for r in cursor.fetchall():
        addr = (r[2]).strip() + "\n" + r[3].strip() + "\n"
        if len(str(r[4]).strip()) > 0:
            addr = addr + r[4].strip() + "\n"
        addr = addr + r[5] + "\n\n"
        addr = addr + "เลขที่ผู้เสียภาษี " + r[6]
    addr = addr if len(addr) > 0 else 'ไม่พบข้อมูลที่อยู่บริษัทครับ!!! รบกวนให้ข้อมูลผมใหม่นะครับ'
    return addr

def getExtNumber(dep_id):

    username = "vpcbot"
    passwd = "vpcbotvpcbot"
    host_name = "vpc-group.dyndns-office.com"
    db_name = "vpcbot"
    info_emoji = u'\U00002139'
    telephone_emoji = u'\U0000260E'


    conn = connection.MySQLConnection(user=username, password=passwd,
                                          host=host_name, database=db_name)
    cursor = conn.cursor()

    cursor.execute("SELECT dep_name, first_name, ext_number, email FROM vpcbot.users WHERE LENGTH(ext_number)>0 AND dep_name LIKE %s  ORDER BY dep_name, ext_number", ('%' + dep_id + '%',))
    ext_number = ""
    isFirst = 1
    ifLab = 1 if (dep_id.find("LAB")>=0) else 0
    oDepName = ""
    for r in cursor.fetchall():
        #print(r)
        if isFirst :
           if ifLab:
              ext_number = info_emoji + " เบอร์ติดต่อภายในของ LAB\n"
           else:
               ext_number = info_emoji + " เบอร์ติดต่อภายในของ " + r[0] + "\n"
        if ifLab:
            if isFirst == 0 and r[0].strip() != oDepName:
                ext_number +="\n"
                ext_number +=  r[1].strip()+ " " + r[0] +" " + telephone_emoji +" "+ r[2].strip()
            else:
                ext_number +=  r[1].strip()+ " " + r[0] +" " + telephone_emoji +" "+ r[2].strip()
            oDepName = r[0].strip()
        else:
            ext_number +=  r[1].strip()+ " " + telephone_emoji +" "+ r[2].strip()
        isFirst = 0

        '''
        if len(r[3].strip()) > 0:
           ext_number += " Email  "+r[3]
        '''
        ext_number +=  "\n"
    ext_number = ext_number if len(ext_number) > 0 else 'ไม่มีแผนก '+dep_id+' ครับ !!! '

    return ext_number

if __name__ == "__main__":
    app.run()