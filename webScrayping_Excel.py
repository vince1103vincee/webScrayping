from urllib.request import urlopen, urlretrieve
from urllib.error import HTTPError
from bs4 import BeautifulSoup

import pandas as pd
df = pd.DataFrame(columns=["Picture", "Stars", "Number of Reviews", "Average Cost", "Japanese Name", "English Name", "URL"])
import warnings           
warnings.filterwarnings('ignore')

from StyleFrame import StyleFrame
import glob
import openpyxl
from openpyxl import load_workbook
from openpyxl.drawing import image
import os

import requests as rq
ExcelDataLocation = 'tablelog.xlsx'
pictureFolder = 'tablelog/'

page = 1
while (page<=1):
    
    url = "https://tabelog.com/tw/osaka/rstLst/"+str(page)+"/?SrtT=rt"
    print("Processing : ", url)

    try: 
        nl_response = rq.get(url)
        
    except HTTPError:
        print("Completed")
        break

    soup = BeautifulSoup(nl_response.text, 'lxml')
    print("Scrayping page " + str(page))

    for p in soup.findAll('li', {'class': 'list-rst'}):
        jap = p.find('small', {'class': 'list-rst__name-ja'})
        eng = p.find('a', {'class': 'list-rst__name-main'})
        scores = p.find_all('b', {'class': 'c-rating__val'})
        reviewNumber = p.find('b', {'class': ''})
        price = p.find('li', {'class': 'c-rating--sm'}).find('span', {'class': 'c-rating__val'})
        img = p.find('img', {'class': 'c-img'})
        #print(img["src"])
        fname = pictureFolder + img["src"].split("/")[-1]
        urlretrieve(img["src"], fname)

        print(jap.text)
        print(eng.text)
        print(scores[0].text)
        print(reviewNumber.text)
        print(price.text)
        print(eng["href"])
        print("")
       
        s = pd.Series([scores[0].text, reviewNumber.text, price.text, jap.text, eng.text, eng["href"]],
                      index=["Stars", "Number of Reviews", "Average Cost", "Japanese Name", "English Name", "URL"])
        # 因為 Series 沒有橫列的標籤, 所以加進去的時候一定要 ignore_index=True
        df = df.append(s, ignore_index=True)

    page = page + 1

print("WebScrayping Completed.")

sf = StyleFrame(df) # 轉成StyleFrame格式

sf.set_column_width_dict(col_width_dict = { # 設定列寬
    ("Picture"): 25.5,
    ("Stars", "Number of Reviews", "Average Cost", "Japanese Name", "English Name"): 20,
    ("URL"): 65.5
})

# 設定行高
all_rows = sf.row_indexes
sf.set_row_height_dict(row_height_dict = { all_rows[1:]: 120})

# 將資料存入Excel檔
sf.to_excel( ExcelDataLocation,
             sheet_name = 'Sheet1',
             right_to_left = False,
             columns_and_rows_to_freeze = 'A1',
             row_to_add_filters = 0).save()

print('Data Saved to ' + ExcelDataLocation)

col = 0
wb = load_workbook(ExcelDataLocation)
ws = wb.worksheets[0]

#圖片依取得時間排序
searchedfiles = sorted(glob.glob(pictureFolder + '*.jpg'), key = os.path.getmtime) #圖片依取得時間排序

# 將圖片匯入Excel檔
for fn in searchedfiles:
    img = openpyxl.drawing.image.Image(fn)
    c = str(col+2)
    ws.add_image(img, 'A' + c)
    col = col +1
wb.save(ExcelDataLocation)
print('Images Saved to' +  ExcelDataLocation)

"""
# 用urlopen的寫法
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
       
        s = pd.Series([scores[0].text, reviewNumber.text, price.text, jap.text, eng.text, eng["href"]],
                      index=["綜合評分", "評分筆數", "平均價錢", "日文店名", "英文店名", "介紹網址"])
        # 因為 Series 沒有橫列的標籤, 所以加進去的時候一定要 ignore_index=True
        #df = df.append(s, ignore_index=True)

    page = page +1

print("WebScrayping Completed.")
"""