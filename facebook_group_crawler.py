'''
使用 selenium 控制瀏覽器的方式爬取社團的文章
因為臉書要往下滑他才會繼續加載下面的內容，所以我們要先把整個社團的文章和留言都展開，然後一次抓資料
'''

# 需要的套件，還沒下載記得先下載
# pip install selenium

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

# Facebook網址!
url = 'https://www.facebook.com'

# 透過Browser Driver 開啟 Chrome
'''
要讓selenium能夠控制瀏覽器，要先下載瀏覽器相對應的webdriver，這裡以google為例
先到chrome首頁，點右上角三個點點，進入chrome設定，到設定後點選左下角的 關於chrome ，找到chrome版本，我的是87.0.4280.88。
接著到 https://chromedriver.chromium.org/downloads 下載你的版本對應的chromedriver，我下載了chromedriver_win32.zip這個。
解壓縮後把exe執行檔放到你要的位置，更改下面的絕對位置就可以使用了
'''
driver = webdriver.Chrome("D:/NCKU/109-1/computational_thinking/code/chromedriver_win32/chromedriver.exe")
# 到這一步先run，如果程式不能正常打開瀏覽器可以私訊我 !!!


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
#模擬使用者，這裡讓他等2秒再繼續執行
time.sleep(2)


# 檢查有沒有被擋下來
if len(driver.find_elements_by_xpath("//*[contains(text(), '你的帳號暫時被鎖住')]")) > 0:
    driver.find_elements_by_xpath("//*[contains(text(), '是')]")[1].click()

# 切換頁面到運算思維社團，這一步網頁可能會跳出facebook想要傳送通知是或否的視窗，要手動關掉，不然頁面會一直停在這裡
spec_url = 'https://www.facebook.com/groups/315124296585941'
driver.get(spec_url)

# 建立scroll function滑到最底
def scroll(scrolltimes):
    for i in range(scrolltimes):
        # 每一次頁面滾動都是滑到網站最下方
        js = 'window.scrollTo(0, document.body.scrollHeight);'
        driver.execute_script(js)
        time.sleep(1)

# 呼叫scroll function，就會直接滾動頁面。這裡設50次是因為我大概算過滑到最底需要加載50次
scroll(50)

# ----------解析網站------------
# BeautifulSoup是爬蟲需要的套件，第一次使用先 pip install BeautifulSoup4
from bs4 import BeautifulSoup
soup = BeautifulSoup(driver.page_source,"html.parser")

'''
到臉書社團頁面，按F12查看網頁原始碼。
在右邊那欄的左上角有個方框包箭頭的地方"select an element in the page to inspect it"，
點他然後在左邊臉書頁面找貼文對應到的div是什麼。
你會發現每一篇貼文都是被包在<div class=du4w35lb k4urcfbm l9j0dhe7 sjgh65i0></div>區塊裡的，所以我們要抓出社團裡所有的貼文區塊
網頁組成分為html, javascript, css。html負責呈現網頁內容，css排版，javascript則是和使用者互動。
詳細的網頁教學上網搜尋一下就有很詳盡的解釋了！
'''
frames = soup.find_all(class_='du4w35lb k4urcfbm l9j0dhe7 sjgh65i0')

# ---------展開所有留言---------請耐心等待
'''
我們剛才已經把整個網頁滑到最底，接下來我們要展開每篇貼文的留言
'''
import selenium.webdriver.support.ui as ui
for i in range(100):
    try:
        # 找找看展開留言的class是什麼，記得要找role='button'的那一個標籤喔
        element = driver.find_elements_by_class_name("oajrlxb2.bp9cbjyn.g5ia77u1.mtkw9kbi.tlpljxtp.qensuy8j.ppp5ayq2.goun2846.ccm00jje.s44p3ltw.mk2mc5f4.rt8b4zig.n8ej3o3l.agehan2d.sk4xxmp2.rq0escxv.nhd2j8a9.pq6dq46d.mg4g778l.btwxx1t3.g5gj957u.p7hjln8o.kvgmc6g5.cxmmr5t8.oygrvhab.hcukyx3x.tgvbjcpo.hpfvmrgz.jb3vyjys.p8fzw8mz.qt6c0cv9.a8nywdso.l9j0dhe7.i1ao9s8h.esuyzwwr.f1sip0of.du4w35lb.lzcic4wl.abiwlrkh.gpro0wi8.m9osqain.buofh1pr")
        # 每展開一次流言就要重解析一次網頁
        soup = BeautifulSoup(driver.page_source,"html.parser")
        # content是「展開一則留言」、「XXX已回覆」這類的字
        content = soup.find_all(class_ = 'oajrlxb2 bp9cbjyn g5ia77u1 mtkw9kbi tlpljxtp qensuy8j ppp5ayq2 goun2846 ccm00jje s44p3ltw mk2mc5f4 rt8b4zig n8ej3o3l agehan2d sk4xxmp2 rq0escxv nhd2j8a9 pq6dq46d mg4g778l btwxx1t3 g5gj957u p7hjln8o kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x tgvbjcpo hpfvmrgz jb3vyjys p8fzw8mz qt6c0cv9 a8nywdso l9j0dhe7 i1ao9s8h esuyzwwr f1sip0of du4w35lb lzcic4wl abiwlrkh gpro0wi8 m9osqain buofh1pr')
        print(i)
        # 這裡略過開頭是「隱藏」的是因為我發現「展開所有11則留言」的button和「隱藏11則回覆」的button是完全一樣的，
        # 如果沒有略過開頭是「隱藏」的留言的話，網頁就會一直展開11則留言、隱藏11則留言、展開11則留言……直到for迴圈跑完
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


# 展開所有流言就整個網頁就變成靜態了，我們要開始爬貼文標題和留言~~~
# 照慣例
# pip install Pandas
# pip install numpy
import csv
import pandas as pd
import numpy as np

#-------------------開始爬作業的title和下方留言---------------------------

# 建立一個空的list
contents = []

# 因為展開了所有留言，要再解析一次
soup = BeautifulSoup(driver.page_source, "html.parser")
frames = soup.find_all(class_='du4w35lb k4urcfbm l9j0dhe7 sjgh65i0')

# 爬到的資料要存在csv檔裡，pandas的DataFrame很好用。test_csv.csv是我已經手動新增的一個檔案，裡面有30個人的選課資訊。test_csv.csv有附上可參考
with open('D:/NCKU/109-1/computational_thinking/code/test_csv.csv', encoding='utf-8') as response:
    csv_table = csv.reader(response)
    df = pd.DataFrame(csv_table)
    df.columns = df.iloc[0]
    df = df.reindex(df.index.drop(0))
    for i in frames:
        # content是文章的第一行的內容，我們要找 [ HW_Submission_xxxxx ]的貼文
        content = i.find('div', dir='auto')
        if content == None:
            continue
        if content.text[0:15] == "[ HW Submission":
            idx = content.text.find("]")
            title = content.text[0:idx + 1]
            df[title] = "0"
            contents.append(title)

            # 抓留言
            messages = i.find('ul').find_all('li', recursive=False) # recursive=False是只往下找一層的意思，不會找到第二層。因為我們只需要留言，不需要留言的回覆
            for num1 in messages:
                message = num1.find('div').find(class_='ecm0bbzt e5nlhep0 a8c37x1j').find('div',
                                                                                          class_='kvgmc6g5 cxmmr5t8 oygrvhab hcukyx3x c1et5uql').find(
                    dir='auto').text

                # 原本的判斷方式應該是有沒有「HW_B54066067_沈姵昕」這一行，這裡因為各個作業繳交區的格式其實沒有很統一，
                # 所以判斷方式改為留言第一句有沒有包含名字就好了
                for i in range(30):
                    if message.find(df.loc[i + 1, 'NAME']) == -1:
                        pass
                    else:
                        df.loc[i + 1, title] = 1

    # 171到180行是為了判斷替代作業有幾次，方便等下統計作業完成度。
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

        elif df.loc[i + 1, "alternative_hw"] == '1' and k == 0: # 選擇替代作業的人，但是還沒開作業繳交區的情況
            df.loc[i + 1, 'hw_finished'] = "還沒開作業繳交區!"
        else:
            temp = df.iloc[i, 4:4 + num_of_hw].values
            temp2 = temp.astype(int)
            finished = np.sum(temp2) / (num_of_hw - k)
            df.loc[i + 1, 'hw_finished'] = int(finished * 100)

    #存成csv檔
    df.to_csv('D:/NCKU/109-1/computational_thinking/code/final_record.csv', index=False)
