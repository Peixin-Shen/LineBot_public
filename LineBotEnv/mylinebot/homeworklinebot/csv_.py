# -*- coding: utf-8 -*-


import requests
import csv
import pandas as pd


if __name__ == '__main__':
    with open('C:/Users/Peixin/Downloads/1213.csv', encoding="utf-8") as response:
        print(type(response))
        csv_table = csv.reader(response)
        # header = next(csv_table)  # 略過第一個row
        df = pd.DataFrame(csv_table)  # 轉成dataframe
        df.columns = df.iloc[0]  # 第一個row當作column name
        df = df.reindex(df.index.drop(0))  # drop掉被拿來當column name的那一列
        name = '陳怡真'
        # print(df)
        out_df = df[df.loc[:, "Name"] == name]
    # print(out_df['data camp'].values[0])
    print(df['userLineID'])
