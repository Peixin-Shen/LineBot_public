# coding: utf-8

from __future__ import unicode_literals
import csv
import pandas as pd
import requests
import json
import numpy as np
import random
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import (
    MessageEvent,
    TextMessage,
    TextSendMessage,
    TemplateSendMessage,
    ButtonsTemplate,
    MessageTemplateAction
)
import configparser


app = Flask(__name__)
# app.config["host"] = "0.0.0.0"

# line bot 的 access token 存在 config.ini 檔裡
config = configparser.ConfigParser()
config.read('config.ini')
line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))




# ---------richmenu---------------

headers = {"Authorization":"Bearer 6DUyjBVG+UgqDr9uEvtVljCVFZMOTcLpay8EHJf3q7mdPwwvy5e1busDaXgLm3ptMiOEugyFLPqvH8I3+7i19X2hjXTeXm3PFSEAyvmAfYUGdpwRj8+CVv7wrBUqNhc9RZY0ec0SPFXHqf0yXJp2NQdB04t89/1O/w1cDnyilFU=","Content-Type":"application/json"}

body = {
    "size": {"width": 2500, "height": 843},
    "selected": "true",
    "name": "功能選單",
    "chatBarText": "查看更多功能",
    "areas":[
    {
      "bounds": { "x": 0, "y": 0, "width": 839, "height": 843 },
      "action": { "type": "message", "text": "傳提醒" }
    },
    {
      "bounds": { "x": 838, "y": 0, "width": 829, "height": 843 },
      "action": { "type": "message", "text": "查詢功能" }
    },
    {
      "bounds": { "x": 1662, "y": 0, "width": 838, "height": 843 },
      "action": { "type": "message", "text": "講笑話" }
    }
    ]
  }

req = requests.request('POST', 'https://api.line.me/v2/bot/richmenu',
                       headers=headers,data=json.dumps(body).encode('utf-8'))
a = req.text[15:56]

with open("D:/NCKU/109-1/computational_thinking/code/controller.jpg", 'rb') as f:
    line_bot_api.set_rich_menu_image(a, "image/jpeg", f)

req = requests.request('POST', 'https://api.line.me/v2/bot/user/all/richmenu/'+a,
                       headers=headers)

# ----------richmenu-end-----------------------

# 隨機回傳一則笑話
def joke():
    with open('D:/NCKU/109-1/computational_thinking/code/joke.csv', encoding="utf-8") as response:
        csv_table = csv.reader(response)
        df = pd.DataFrame(csv_table)
        random_int = random.randint(0,df.shape[0]-1)
        joke_ = df[random_int:random_int+1]
        joke_array = np.array(joke_)
        joke_list = joke_array[0].tolist()
        joke_list = [x for x in joke_list if x != '']
    return joke_list

# 查詢作業總成績
def search_grade(LINE_ID):
    with open('D:/NCKU/109-1/computational_thinking/code/grade_1213.csv', encoding="utf-8") as response:
        #寫入userLineID
        # writer = csv.writer(response)
        csv_table = csv.reader(response)
        # header = next(csv_table)  # 略過第一個row
        df = pd.DataFrame(csv_table)  # 轉成dataframes
        df.columns = df.iloc[0]  # 第一個row當作column name
        df = df.reindex(df.index.drop(0))  # drop掉被拿來當column name的那一列
        # -----前面不用動
        try:
            out_df = df[df.loc[:, "line_id"] == LINE_ID ]
            grade_value = out_df['Sum'].values[0]
        except:
            grade_value = '你還沒有輸入名字喔！請輸入名字，格式：我是OOO'
    return grade_value

# 註冊
def register_lineid(name, studentID, LINE_ID):
    with open('D:/NCKU/109-1/computational_thinking/code/grade_1213.csv', encoding="utf-8") as response:
        csv_table = csv.reader(response)
        df = pd.DataFrame(csv_table)
        df.columns = df.iloc[0]
        df = df.reindex(df.index.drop(0))
        for i in range(30):

            if (df.loc[i + 1, 'Name'] == name):
                if df.loc[i + 1, 'ID'] == studentID:
                    if df.loc[i + 1, 'line_id'] == '':
                        df.loc[i + 1, 'line_id'] = LINE_ID
                        success_message = '成功紀錄！請從選單點選要使用的功能'
                    elif df.loc[i + 1, 'line_id'] == LINE_ID:
                        success_message = '你已經註冊過囉！'
                    else:
                        success_message = '此用戶已被註冊！這不是你，請聯絡管理人'
                else:
                    success_message = '學號輸入錯誤，學號開頭請用大寫英文字母，請再輸入一次。格式：'+'\n'+'姓名：王小明/學號：B54012312'
                break
            else:
                success_message = '修課名單找不到這個名字，請重新輸入。格式：'+'\n'+'姓名：王小明/學號：B54012312'
        df.to_csv('D:/NCKU/109-1/computational_thinking/code/1212.csv', index=False)

    with open('D:/NCKU/109-1/computational_thinking/hw_linebot/final_record.csv', encoding="utf-8") as response:
        csv_table = csv.reader(response)
        df = pd.DataFrame(csv_table)
        df.columns = df.iloc[0]
        df = df.reindex(df.index.drop(0))
        for i in range(30):

            if (df.loc[i + 1, 'NAME'] == name):
                if df.loc[i + 1, 'Student_ID'] == studentID:
                    if df.loc[i + 1, 'LINE_ID'] == '':
                        df.loc[i + 1, 'LINE_ID'] = LINE_ID
                        success_message = '成功紀錄！請從選單點選要使用的功能'
                    elif df.loc[i + 1, 'LINE_ID'] == LINE_ID:
                        success_message = '你已經註冊過囉！'
                    else:
                        success_message = '此用戶已被註冊！這不是你，請聯絡管理人'
                else:
                    success_message = '學號輸入錯誤，學號開頭請用大寫英文字母，請再輸入一次。格式：'+'\n'+'姓名：王小明/學號：B54012312'
                break
            else:
                success_message = '修課名單找不到這個名字，請重新輸入'

        df.to_csv('D:/NCKU/109-1/computational_thinking/hw_linebot/final_record.csv', index=False)

    return success_message

# 作業完成度、未交作業
class Homework:
    def __init__(self, LINE_ID):
        with open('D:/NCKU/109-1/computational_thinking/hw_linebot/final_record.csv', encoding="utf-8") as response:
            csv_table = csv.reader(response)
            df = pd.DataFrame(csv_table)
            df.columns = df.iloc[0]
            df = df.reindex(df.index.drop(0))
            self.df = df
            self.LINE_ID = LINE_ID
            print(self.LINE_ID)

    def finished_percent(self):
        try:
            out_df = self.df[self.df.loc[:, "LINE_ID"] == self.LINE_ID]
            finished_percent = out_df['hw_finished'].values[0] +'%'
            # print(finished_percent)
        except:
            finished_percent = '你還沒有輸入名字喔！請輸入名字，格式：' + '\n' + '姓名：王小明/學號：B54012312'
        return finished_percent

    def unfinished(self):
        hw_unfinished_ = []
        try:
            out_df = self.df[self.df.loc[:, "LINE_ID"] == self.LINE_ID]
            h = 0
            g = 0
            for t in self.df.columns[4:-1]:
                if out_df[t].values[0] == '0':
                    g = g + 1
                    hw_unfinished_.append(t)
                    h = '還沒交的作業' + '\n'
                    for num_ in hw_unfinished_:
                        h = h + num_ + '\n'
                else:
                    pass
            if g == 0:
                h = '所有作業都完成囉！'
        except:
            h = '你還沒有輸入名字喔！請輸入名字，格式：' + '\n' + '姓名：王小明/學號：B54012312'
        return h



@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']

    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        # print(body, signature)
        handler.handle(body, signature) # 跟parse的差別??

    except InvalidSignatureError:
        abort(400)

    return 'OK'



@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text[0:2] == '姓名':
        name_start = event.message.text.rfind('姓名')
        name_end = event.message.text.find('/')
        Name = event.message.text[name_start + 3:name_end]
        studentID_start = event.message.text.rfind('學號')
        studentID_end = event.message.text.rfind('學號') + 12
        student_ID = event.message.text[studentID_start + 3:studentID_end]
        i = register_lineid(name=Name, studentID=student_ID, LINE_ID=event.source.user_id)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=i)
        )

    elif event.message.text == "查詢功能":
        buttons_template = TemplateSendMessage(
            alt_text='查詢功能',
            template=ButtonsTemplate(
                title='查詢之功能',
                text='選擇你所想要查詢之功能',
                actions=[
                    MessageTemplateAction(
                        label='作業成績',
                        text='作業成績'
                    ),
                    MessageTemplateAction(
                        label='作業完成度',
                        text='作業完成度'
                    ),
                    MessageTemplateAction(
                        label='未交作業',
                        text='未交作業'
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, buttons_template)

    elif event.message.text == '作業成績':
        b = search_grade(event.source.user_id)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=b)
        )
    elif event.message.text == '作業完成度':
        d1 = Homework(LINE_ID=event.source.user_id)
        d = d1.finished_percent()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=d)
        )
    elif event.message.text == '講笑話':
        e = joke()
        string = ''
        for i in e:
            string += i
            string += '\n'
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=string)
        )
    elif event.message.text == '未交作業':
        g1 = Homework(LINE_ID=event.source.user_id)
        g = g1.unfinished()

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=g)
        )
    else:
        e = joke()
        string = ''
        for i in e:
            string += i
            string += '\n'
        f = '我看不懂你在說什麼，請輸入' + '\n' + '「查詢功能」' + '\n' + '來查看可以使用的功能。' + '\n' + '講個笑話給你聽吧！' + '\n' + '\n' + '\n' + string
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=f)
        )


if __name__ == "__main__":
    app.run()