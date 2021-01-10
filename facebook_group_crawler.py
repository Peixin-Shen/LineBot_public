from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

# Facebook網址!
url = 'https://www.facebook.com'

# 透過Browser Driver 開啟 Chrome
driver = webdriver.Chrome("D:/NCKU/109-1/computational_thinking/code/chromedriver_win32/chromedriver.exe")

# 放大視窗
driver.maximize_window()

# 前往facebook
driver.get(url)

# 關閉網頁，暫時用不到這一行
#driver.close()

# 登入的帳號與密碼，這裡寫死
username = '--------------@gmail.com'
password = '------'

# 不寫死的方法
# username = input('帳號，輸完按enter：')
# password = input('密碼，輸完按enter：')

# 輸入帳號密碼並登入
WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="email"]')))
elem = driver.find_element_by_id("email")
elem.send_keys(username)
elem = driver.find_element_by_id("pass")
elem.send_keys(password)
elem.send_keys(Keys.RETURN)
time.sleep(3)


# 檢查有沒有被擋下來
if len(driver.find_elements_by_xpath("//*[contains(text(), '你的帳號暫時被鎖住')]")) > 0:
    driver.find_elements_by_xpath("//*[contains(text(), '是')]")[1].click()

# 切換頁面到運算思維社團
spec_url = 'https://www.facebook.com/groups/315124296585941'
driver.get(spec_url)

# 建立scroll function滑到最底
def scroll(scrolltimes):
    for i in range(scrolltimes):
        # 每一次頁面滾動都是滑到網站最下方
        js = 'window.scrollTo(0, document.body.scrollHeight);'
        driver.execute_script(js)
        time.sleep(1)

# 呼叫scroll function，就會直接滾動頁面
scroll(50)

# ----------解析網站------------
from bs4 import BeautifulSoup
soup = BeautifulSoup(driver.page_source,"html.parser")
frames = soup.find_all(class_='du4w35lb k4urcfbm l9j0dhe7 sjgh65i0')

# ---------展開所有留言---------超慢...
import selenium.webdriver.support.ui as ui
#element = driver.find_element_by_class_name("d2edcug0.hpfvmrgz.qv66sw1b.c1et5uql.rrkovp55.a8c37x1j.keod5gw0.nxhoafnm.aigsh9s9.d3f4x2em.fe6kdd0r.mau55g9w.c8b282yb.iv3no6db.jq4qci2q.a3bd9o3v.lrazzd5p.m9osqain")
#"oajrlxb2.bp9cbjyn.g5ia77u1.mtkw9kbi.tlpljxtp.qensuy8j.ppp5ayq2.goun2846.ccm00jje.s44p3ltw.mk2mc5f4.rt8b4zig.n8ej3o3l.agehan2d.sk4xxmp2.rq0escxv.nhd2j8a9.pq6dq46d.mg4g778l.btwxx1t3.g5gj957u.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.tgvbjcpo.hpfvmrgz.jb3vyjys.p8fzw8mz.qt6c0cv9.a8nywdso.l9j0dhe7.i1ao9s8h.esuyzwwr.f1sip0of.du4w35lb.lzcic4wl.abiwlrkh.gpro0wi8.m9osqain.buofh1pr")
for i in range(100):
    try:
        element = driver.find_elements_by_class_name("oajrlxb2.bp9cbjyn.g5ia77u1.mtkw9kbi.tlpljxtp.qensuy8j.ppp5ayq2.goun2846.ccm00jje.s44p3ltw.mk2mc5f4.rt8b4zig.n8ej3o3l.agehan2d.sk4xxmp2.rq0escxv.nhd2j8a9.pq6dq46d.mg4g778l.btwxx1t3.g5gj957u.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.tgvbjcpo.hpfvmrgz.jb3vyjys.p8fzw8mz.qt6c0cv9.a8nywdso.l9j0dhe7.i1ao9s8h.esuyzwwr.f1sip0of.du4w35lb.lzcic4wl.abiwlrkh.gpro0wi8.m9osqain.buofh1pr")
        soup = BeautifulSoup(driver.page_source,"html.parser")
        content = soup.find_all(class_ = 'oajrlxb2 bp9cbjyn g5ia77u1 mtkw9kbi tlpljxtp qensuy8j ppp5ayq2 goun2846 ccm00jje s44p3ltw mk2mc5f4 rt8b4zig n8ej3o3l agehan2d sk4xxmp2 rq0escxv nhd2j8a9 pq6dq46d mg4g778l btwxx1t3 g5gj957u p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x tgvbjcpo hpfvmrgz jb3vyjys p8fzw8mz qt6c0cv9 a8nywdso l9j0dhe7 i1ao9s8h esuyzwwr f1sip0of du4w35lb lzcic4wl abiwlrkh gpro0wi8 m9osqain buofh1pr')
        print(i)
        if content[0].text[:2]=="隱藏":
            del(element[0])
            del(content[0])
        else:
            pass
        driver.execute_script("arguments[0].click();", element[0])
        time.sleep(1)
        i=i+1
    except:
        print('結束了')
        break



import csv
import pandas as pd
import numpy as np

#-------------------開始爬作業的title和下方留言---------------------------

# 建立一個空的list
contents = []

# 因為展開了所有留言，要再解析一次
soup = BeautifulSoup(driver.page_source, "html.parser")
frames = soup.find_all(class_='du4w35lb k4urcfbm l9j0dhe7 sjgh65i0')

with open('D:/NCKU/109-1/computational_thinking/code/test_csv.csv', encoding='utf-8') as response:
    csv_table = csv.reader(response)
    df = pd.DataFrame(csv_table)
    df.columns = df.iloc[0]
    df = df.reindex(df.index.drop(0))
    for i in frames:
        content = i.find('div', dir='auto')
        if content == None:
            continue
        if content.text[0:15] == "[ HW Submission":
            idx = content.text.find("]")
            title = content.text[0:idx + 1]
            df[title] = "0"
            contents.append(title)
            #             thumb = i.find('span', class_="pcp91wgn") #抓讚數

            # 抓留言......
            messages = i.find('ul').find_all('li', recursive=False)
            for num1 in messages:
                message = num1.find('div').find(class_='ecm0bbzt e5nlhep0 a8c37x1j').find('div',
                                                                                          class_='kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql').find(
                    dir='auto').text
                for i in range(30):
                    if message.find(df.loc[i + 1, 'NAME']) == -1:
                        pass
                    else:
                        df.loc[i + 1, title] = 1

    num_of_hw = len(contents)
    df['hw_finished'] = 0
    k = 0
    alter_num = []
    for i in contents:
        if i.find('Alternative') == -1:
            pass
        else:
            k = k + 1
            alter_num.append(i)

    for i in range(30):
        if df.loc[i + 1, "alternative_hw"] == '1' and k != 0:  # 代表是做替代作業的人，且有開作業繳交區
            ee = 0
            for q in alter_num:
                df.loc[i + 1, 'hw_finished'] = int((ee + int(df.loc[i + 1, q])) / len(alter_num) * 100)
                ee = ee + int(df.loc[i + 1, q])

        elif df.loc[i + 1, "alternative_hw"] == '1' and k == 0:
            df.loc[i + 1, 'hw_finished'] = "還沒開作業繳交區!"
        else:
            temp = df.iloc[i, 4:4 + num_of_hw].values
            temp2 = temp.astype(int)
            finished = np.sum(temp2) / (num_of_hw - k)
            df.loc[i + 1, 'hw_finished'] = int(finished * 100)
    #存成csv檔
    df.to_csv('D:/NCKU/109-1/computational_thinking/code/final_record.csv', index=False)
