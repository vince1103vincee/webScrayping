#python web scrayping 教學示範
#抓取 結婚吧 網站("https://www.marry.com.tw/venue-shop-kwbt2004mmir0mmpg")中的業者資料
#請先輸入pip install request; pip install BeautifulSoup; pip install lxml
import requests as rq
from bs4 import BeautifulSoup
import io
import time

def sleeptime(hour, mi, sec):
    return hour*3600 + mi*60 + sec

tStart = time.time() 
fp = io.open("marryData-List.txt", "ab+") 
"""
marryData-List.txt 為開啟或編輯檔案
第二個參數"ab+"為[打開可追加和讀寫的二進制文件，若無此文件則建立] (a: append, b: binary, +: 可讀)
其他可用參數:
"r" : 打開指定文件，若無此文件則報錯(read)，加上"+"代表加上write功能
"w" : 打開指定文件，若文件已存在，會直接覆蓋原內容(write)，加上"+"代表加上read功能
"""
i = 1

while (i<=1): #i要抓取的頁數
    nextlink = "https://www.marry.com.tw/venue-shop-kwbt2004mmir0mmpg" + str(i) + "mm"
    nl_response = rq.get(nextlink)  #利用get指令抓取網站上的資料
    soup = BeautifulSoup(nl_response.text, "lxml") #將網站內容以lxml處理，並回傳至soup
    print("Scrayping page " + str(i))
    u = 1
    for url in soup.findAll('a', {'class': 'shop_name'}): #找出soup中所有含有<a class="shop_name">的內容並存入url
        response = rq.get(url.get('href')) #將url中的連結目的(herf)傳入response
        html_doc = response.text
        soup = BeautifulSoup(response.text, "lxml") #將連結目的的網站內容以lxml處理，並傳至soup
        print("Scrayping company: " + str(u))
        if soup.select('h1') != []: 
            company = soup.select('h1')[0].find('a').text #找出soup中的第一筆<h1>，並將其<a>中的文字傳給company

            if company != '':
                pid = soup.findAll('li', {'class': 'icon-check'}) 
                #找出soup中所有<li class="icon-check">的內文，並傳入pid
                Con = ",".join([p.text.strip() for p in pid]) 
                #將pid中的項目全部合併，並在每個項目中間插入","
                #strip()是把文字中的空白刪除
                address = soup.findAll('ul', {'class': 'contacts_list'})[0].find('span',{'class': 'contacts_info'}).text
                #找出公司地址並寫入address
                fp.write(company.encode('utf-8') + '='.encode('utf-8'))
                fp.write(Con.encode('utf-8')+ '?'.encode('utf-8') + address.encode('utf-8'))
                fp.write('\n'.encode('utf-8'))
                #將資料寫入檔案內
                time.sleep(sleeptime(0,0,10))
                #暫停一段時間，以免被網頁誤認為惡意攻擊
        u = u +1 
    print("Page " + str(i) + "completed")
    i= i+1
tEnd = time.time()
fp.close()
print("It costs %f sec" % (tEnd-tStart))
        
