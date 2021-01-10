from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)
import requests
import csv
import pandas as pd
import json
from random import choice

# --------

def csv_(name,orient='split'):
    with open('D:/NCKU/109-1/computational_thinking/code/final_record.csv', encoding="utf-8") as response:
        #寫入userLineID
        # writer = csv.writer(response)
        csv_table = csv.reader(response)
        # header = next(csv_table)  # 略過第一個row
        df = pd.DataFrame(csv_table)  # 轉成dataframe
        df.columns = df.iloc[0]  # 第一個row當作column name
        df = df.reindex(df.index.drop(0))  # drop掉被拿來當column name的那一列
        #-----前面不用動
        out_df = df[df.loc[:, "NAME"] == name]
    return out_df['hw_finished'].values[0] # json.loads(df_json)


def search_grade(LINE_ID):
    with open('D:/NCKU/109-1/computational_thinking/code/grade_1213.csv', encoding="utf-8") as response:
        #寫入userLineID
        # writer = csv.writer(response)
        csv_table = csv.reader(response)
        # header = next(csv_table)  # 略過第一個row
        df = pd.DataFrame(csv_table)  # 轉成dataframe
        df.columns = df.iloc[0]  # 第一個row當作column name
        df = df.reindex(df.index.drop(0))  # drop掉被拿來當column name的那一列
        # -----前面不用動
        try:
            # df[df.loc[:, "line_id"] == LINE_ID ]:
            out_df = df[df.loc[:, "line_id"] == LINE_ID ]
            grade_value = out_df['Sum'].values[0]
        except:
            grade_value = '你還沒有輸入名字喔！請輸入名字，格式：我是OOO'
    return grade_value


##寫入line_id
def input_lineid(NAME, LINE_ID):
    # 改成學號驗證------------------
    with open('D:/NCKU/109-1/computational_thinking/code/final_record.csv',encoding="utf-8") as response:
        csv_table = csv.reader(response)
        df = pd.DataFrame(csv_table)
        df.columns = df.iloc[0]
        df = df.reindex(df.index.drop(0))
        # success_message = 0
        # print(df)
        # print(df["ID"][1])
        for i in range(30):
            try:
                if (df.loc[i + 1, 'NAME'] == NAME):
                    df.loc[i + 1, 'LINE_ID'] = LINE_ID
                    print(LINE_ID)
                    success_message = '成功紀錄! 請輸入 查詢功能 ，查看可以使用的功能'
                    break
                else:
                    success_message = '修課名單找不到這個名字，請重新輸入'
            except:
                success_message = '修課名單找不到這個名字，請重新輸入'
        df.to_csv('D:/NCKU/109-1/computational_thinking/code/final_record.csv', index=False)

    with open('D:/NCKU/109-1/computational_thinking/code/grade_1213.csv',encoding="utf-8") as response:
        csv_table = csv.reader(response)
        df = pd.DataFrame(csv_table)
        df.columns = df.iloc[0]
        df = df.reindex(df.index.drop(0))
        print(df)
        print(df["ID"][1])
        for i in range(30):
            try:
                if(df.loc[i + 1, 'Name'] == NAME):
                    df.loc[i + 1, 'line_id'] = LINE_ID
                    print(LINE_ID)
                    # success_message = '成功紀錄! 請輸入 查詢功能 ，查看可以使用的功能'
                    break
            except:
                # success_message = '修課名單找不到這個名字，請重新輸入'
                break
        df.to_csv('D:/NCKU/109-1/computational_thinking/code/grade_1213.csv', index=False)

    return success_message


def hw_finished_percent(LINE_ID):
    with open('D:/NCKU/109-1/computational_thinking/code/final_record.csv', encoding="utf-8") as response:
        #寫入userLineID
        # writer = csv.writer(response)
        csv_table = csv.reader(response)
        # header = next(csv_table)  # 略過第一個row
        df = pd.DataFrame(csv_table)  # 轉成dataframe
        df.columns = df.iloc[0]  # 第一個row當作column name
        df = df.reindex(df.index.drop(0))  # drop掉被拿來當column name的那一列
        #以上不用動
        try:
            out_df = df[df.loc[:, "LINE_ID"] == LINE_ID ]
            finished_percent = out_df['hw_finished'].values[0]
        except:
            finished_percent = '你還沒有輸入名字喔！請輸入名字，格式：我是OOO'
    return finished_percent

def hw_unfinished(LINE_ID):
    with open('D:/NCKU/109-1/computational_thinking/code/final_record.csv', encoding="utf-8") as response:
        csv_table = csv.reader(response)
        # for col_names in row_csv_table:
        # header = next(csv_table)  # 略過第一個row
        df = pd.DataFrame(csv_table)  # 轉成dataframe
        df.columns = df.iloc[0]  # 第一個row當作column name
        df = df.reindex(df.index.drop(0))  # drop掉被拿來當column name的那一列
        hw_unfinished_ = []
        # 以上不用動
        try:
            out_df = df[df.loc[:, "LINE_ID"] == LINE_ID]
            h = 0
            g = 0
            for t in df.columns[4:-1]:
                if out_df[t].values[0] == '0':
                    g=g+1
                    hw_unfinished_.append(t)
                    h = '還沒交的作業' + '\n'
                    for num_ in hw_unfinished_:
                        h = h + num_ + '\n'
                else:
                    pass
            if g==0:
                h='所有作業都完成囉！'
        except:
            h = '你還沒有輸入名字喔！請輸入名字，格式：我是OOO'

    return h







@csrf_exempt
def callback(request):
    if request.method == 'POST':
        signature = request.META['HTTP_X_LINE_SIGNATURE']
        body = request.body.decode('utf-8')

        try:
            events = parser.parse(body, signature)  # 傳入的事件
        except InvalidSignatureError:
            return HttpResponseForbidden()
        except LineBotApiError:
            return HttpResponseBadRequest()

        for event in events:
            if isinstance(event, MessageEvent):  # 如果有訊息事件
                joke = ['先進船的人會先說什麼' + '\n' + '會說online' + '\n' + '\n'+ '\n'+ '\n'+ '\n'+ '\n'+ '\n' + '\n' + '因為仙境傳說online',
                        '有一天，有一隻深海魚在海裡自由自在得游啊游，但他一點也不開心，為什麼?' + '\n'+ '\n'+ '\n'+ '\n'+ '\n'+'\n'+'\n'+'\n' '因為他壓力好大']
                if event.message.text[0:2] == '我是':
                    a = input_lineid(NAME=event.message.text[2:], LINE_ID=event.source.sender_id)
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                    event.reply_token,
                    TextSendMessage(text=a)
                    )

                elif event.message.text == '傳提醒':
                    line_bot_api.push_message('Uc2a7965147869ebe3b5febb6fb3737a4', TextSendMessage(text='hello world!'))

                elif event.message.text == '作業成績':
                    b = search_grade(event.source.sender_id)
                    line_bot_api.reply_message(  # 回復傳入的訊息文字
                        event.reply_token,
                        TextSendMessage(text = b)
                    )

                elif event.message.text == '查詢功能':
                    c='可以使用的功能'+'\n'+'1. 查詢累計作業成績請輸入：作業成績'+'\n'+'2. 查詢作業完成度請輸入：作業完成度'+'\n'+'3. 查詢沒有交的作業：未交作業'
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text = c)
                    )

                elif event.message.text == '作業完成度':
                    d = hw_finished_percent(event.source.sender_id)
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=d+'%')
                    )

                elif event.message.text == '講笑話':
                    e = '不要'
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=e)
                    )
                elif event.message.text == '未交作業':
                    g = hw_unfinished(event.source.sender_id)

                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=g)
                    )
                else:
                    f = '我看不懂你在說什麼，請輸入'+'\n'+'「查詢功能」'+'\n'+'來查看可以使用的功能。'+'\n'+'講個笑話給你聽吧！'+ '\n'+ '\n'+'\n'+choice(joke)
                    line_bot_api.reply_message(
                        event.reply_token,
                        TextSendMessage(text=f)
                )

            else:
                pass
                # line_bot_api.broadcast(
                #     # event.reply_token,
                #     TextSendMessage(text='HI 你好！請先輸入你的全名。格式:我是OOO')
                # )
        return HttpResponse()
    else:
        return HttpResponseBadRequest()