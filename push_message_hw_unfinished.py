import csv
import pandas as pd
import numpy as np

def hw_unfinished(i):
    with open('D:/NCKU/109-1/computational_thinking/code/final_record.csv', encoding="utf-8") as response:
        csv_table = csv.reader(response)
        df = pd.DataFrame(csv_table)
        df.columns = df.iloc[0]
        df = df.reindex(df.index.drop(0))
        hw_unfinished_ = []
        out_df = df[i:i+1]
        if out_df['LINE_ID'].values[0] != '':
            h=0
            g=0
            for t in df.columns[4:-2]:
                if out_df[t].values[0] == '0':
                    g=g+1
                    hw_unfinished_.append(t)
                    h = '還沒交的作業' + '\n'
                    for num_ in hw_unfinished_:
                        h = h + num_ + '\n'
                else:
                    pass
            if g==0:
                h='作業皆已完成'
        else:
            h = '未紀錄'

    message = [out_df['LINE_ID'].values[0], h]
    return message



from linebot import LineBotApi
from linebot.models import TextSendMessage
line_bot_api = LineBotApi('6DUyjBVG+UgqDr9uEvtVljCVFZMOTcLpay8EHJf3q7mdPwwvy5e1busDaXgLm3ptMiOEugyFLPqvH8I3+7i19X2hjXTeXm3PFSEAyvmAfYUGdpwRj8+CVv7wrBUqNhc9RZY0ec0SPFXHqf0yXJp2NQdB04t89/1O/w1cDnyilFU=')
# push message to several users
for i in range(30):
    h = hw_unfinished(i)
    if h[0] != '':
        # print(h[0])
        line_bot_api.push_message(h[0],
            TextSendMessage(text=h[1]))
    else:
        pass