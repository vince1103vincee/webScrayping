from urllib.request import urlopen, urlretrieve
from urllib.error import HTTPError
from bs4 import BeautifulSoup

import pandas as pd
df = pd.DataFrame(columns=["餐廳美圖", "綜合評分", "晚間評分", "年間評分", "日文店名", "英文店名", "介紹網址"])
import warnings
warnings.filterwarnings('ignore')

from StyleFrame import StyleFrame
import glob
import openpyxl
from openpyxl import load_workbook
from openpyxl.drawing import image
import os

page = 1

while (page<=1):
    url = "https://tabelog.com/tw/osaka/rstLst/"+str(page)+"/?SrtT=rt"
    print("Processing : ", url)

    try: 
        response = urlopen(url)
    except HTTPError:
        print("Completed")
        break

    html = BeautifulSoup(response)
    for list in html.find_all("li" , class_="list-rst"): 
        jap = list.find("small" , class_="list-rst__name-ja")
        eng = list.find("a" , class_="list-rst__name-main")
        scores = list.find_all("b" , class_="c-rating__val")
        reviewNumber = list.find("b", class_="")
        price = list.find("li", class_="c-rating--sm").find("span", class_="c-rating__val")
        img = list.find("img" , class_="c-img")
        #print(img["src"])
        fname = "tablelog/" + img["src"].split("/")[-1]
        urlretrieve(img["src"], fname)

        print(jap.text)
        print(eng.text)
        print(scores[0].text)
        print(reviewNumber.text)
        print(price.text)
        print(eng["href"])
        print("")
       
        s = pd.Series([scores[0].text, reviewNumber.text, price.text, jap.text, eng.text, eng["href"].text],
                      index=["綜合評分", "評分筆數", "平均價錢", "日文店名", "英文店名", "介紹網址"])
        # 因為 Series 沒有橫列的標籤, 所以加進去的時候一定要 ignore_index=True
        #df = df.append(s, ignore_index=True)

print("okay")
print(df)