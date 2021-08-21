<<<<<<< HEAD
import requests
from bs4 import BeautifulSoup
import time
import random
import re
import pandas as pd
import pymongo



headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
}

# 建立各項清單
News_Link = []
News_Title = []
News_Type = []
News_Date = []
News_Time = []
News_Content = []
News_ID = []

start_time = time.time()

# 爬取新聞網頁資訊，只爬第一頁
for i in range(1,2):
    url = 'https://www.ettoday.net/news_search/doSearch.php?keywords=香蕉&idx=1&page=' + str(i)
    res = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    print('====== 第 ' + str(i) + ' 頁 ======')
    
    for j in range(0, len(soup.select('div[class=box_2]'))):
        try:
            # 取新聞標題
            title = soup.select('div[class=box_2]')[j].select('h2 a')[0].text
            News_Title.append(re.sub('[-:_、【】。；：)(「」，.&+\n\t\r\u3000]', '', title))
            print(re.sub('[-:_、【】。；：)(「」，.&+\n\t\r\u3000]', '', title))
            
            # 取網址
            link = soup.select('div[class=box_2]')[j].select('h2 a')[0]["href"]
            News_Link.append(link)
#             print(link)
            
            # 建立ID
            news_id = soup.select('div[class=box_2]')[j].select('h2 a')[0]["href"].split('/')[5].split('.')[0]
            News_ID.append(news_id)
#             print(news_id)
            
            # 取新聞類型
            news_type = soup.select('div[class=box_2]')[j].select('span[class=date]')[0].text.split()[0]
            News_Type.append(re.sub('[-:_、【】。；：)(「」，.&+\n\t\r\u3000]', '', news_type))
            print(re.sub('[-:_、【】。；：)(「」，.&+\n\t\r\u3000]', '', news_type))
            
            # 取發布日期
            news_date = soup.select('div[class=box_2]')[j].select('span[class=date]')[0].text.split()[2]
            News_Date.append(news_date)
            print(news_date)
            
            # 取發布時間
            news_time = soup.select('div[class=box_2]')[j].select('span[class=date]')[0].text.split()[3]
            News_Time.append(re.sub('[-_、【】。；：)(「」，.&+\n\t\r\u3000]', '', news_time))
#             print(re.sub('[-_、【】。；：)(「」，.&+\n\t\r\u3000]', '', news_time))
            
            # 取新聞內容
            page_res = requests.get(url=link, headers=headers)
            page_soap = BeautifulSoup(page_res.text, 'html.parser')

            for content in page_soap.select('div[class="story"]'):
                try:
                    News_Content.append(re.sub('[-:_、【】。；：)(「」，.&+\n\t\r\u3000]', ' ', content.text))
                except:
                    pass
            for content in page_soap.select('div[class="story lazyload"]'):
                try:
                    News_Content.append(re.sub('[-:_、【】。；：)(「」，.&+\n\t\r\u3000]', ' ', content.text))
                except:
                    pass
            
        except:
            pass
        
        sleep_time = random.randint(5,10)
        print("sleep time: %s sec"%(sleep_time))
        print('==========')
        time.sleep(sleep_time)
        
print("--- spend %s seconds ---" % (time.time() - start_time))
print('共爬取' + str(len(News_Title)) + '則新聞')



# 要存成 dataframe 的時候，發生爬取資料 array 不一樣的情形
# 用 len 去檢查後，發現 News_Content 的資料多了一筆
# 檢查後將同樣array的資料轉成df1
# News_Data = {'ID':News_ID, '標題':News_Title, '類型':News_Type, '網址':News_Link, '發布日期':News_Date, '發布時間':News_Time }
# df1 = pd.DataFrame(News_Data)

News_Data = {'ID':News_ID, '標題':News_Title, '類型':News_Type, '網址':News_Link, '發布日期':News_Date, '發布時間':News_Time, '內容':News_Content}
df_news_craw = pd.DataFrame(News_Data)

# 將多出一筆的資料存成df2
# df2 = pd.DataFrame({'內容':News_Content})

# 展開所有 row 方便進行交叉比對
# pd.set_option('display.max_rows', None)

# (人工手動)找到重複的部分為index=1372這筆資料，drop掉後重新整理index，並建立成新的dataframe命名為df3
# df3 = df2.drop(df.index[[1372]])
# df3.reset_index(inplace=True, drop=True)

# 將df1和df3用outer join的方式，合併成為需要的dataframe
# df_news_craw = df1.merge(df3, how='outer', left_index=True, right_index=True)

# 進行所需資料清洗，並建立最後要使用的dataframe
news_type1 = df_news_craw['類型'] == '生活'
news_type2 = df_news_craw['類型'] == '政治'
news_type3 = df_news_craw['類型'] == '地方'
news_type4 = df_news_craw['類型'] == '健康'
news_type5 = df_news_craw['類型'] == '財經'
news_type6 = df_news_craw['類型'] == '大陸'
news_type7 = df_news_craw['類型'] == '國際'
news_type8 = df_news_craw['類型'] == '論壇'
news_type9 = df_news_craw['類型'] == 'ETlife'
news_type10 = df_news_craw['類型'] == '其它'

df_banana_news = df_news_craw[(news_type1 | news_type2 | news_type3 | news_type4 | news_type5 | news_type6 | news_type7 | news_type8 | news_type9 | news_type10)]
# df_banana_news_etl.to_csv('東森新聞雲_香蕉.csv', index=False)
print(df_banana_news['標題'])



client = pymongo.MongoClient("mongodb+srv://<username>:<password>@<project_name>.i2omj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.TWFruits
ettoday_news = db.ettoday_news_craw

print("ettoday_news update to mongodb -> start")

for excist_id in df_banana_news['ID']:
    if [x for x in ettoday_news.find({'ID':excist_id})] == []:
        ettoday_news_update = df_banana_news.loc[df_banana_news["ID"]==excist_id].to_dict(orient='records')
        updated = ettoday_news.insert_one(ettoday_news_update[0]).inserted_id
        print("ettoday_news update id", updated)
        
print("ettoday_news update to mongodb -> finish")
=======
import requests
from bs4 import BeautifulSoup
import time
import random
import re
import pandas as pd
import pymongo



headers = {
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
}

# 建立各項清單
News_Link = []
News_Title = []
News_Type = []
News_Date = []
News_Time = []
News_Content = []
News_ID = []

start_time = time.time()

# 爬取新聞網頁資訊，只爬第一頁
for i in range(1,2):
    url = 'https://www.ettoday.net/news_search/doSearch.php?keywords=香蕉&idx=1&page=' + str(i)
    res = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(res.text, 'html.parser')
    print('====== 第 ' + str(i) + ' 頁 ======')
    
    for j in range(0, len(soup.select('div[class=box_2]'))):
        try:
            # 取新聞標題
            title = soup.select('div[class=box_2]')[j].select('h2 a')[0].text
            News_Title.append(re.sub('[-:_、【】。；：)(「」，.&+\n\t\r\u3000]', '', title))
            print(re.sub('[-:_、【】。；：)(「」，.&+\n\t\r\u3000]', '', title))
            
            # 取網址
            link = soup.select('div[class=box_2]')[j].select('h2 a')[0]["href"]
            News_Link.append(link)
#             print(link)
            
            # 建立ID
            news_id = soup.select('div[class=box_2]')[j].select('h2 a')[0]["href"].split('/')[5].split('.')[0]
            News_ID.append(news_id)
#             print(news_id)
            
            # 取新聞類型
            news_type = soup.select('div[class=box_2]')[j].select('span[class=date]')[0].text.split()[0]
            News_Type.append(re.sub('[-:_、【】。；：)(「」，.&+\n\t\r\u3000]', '', news_type))
            print(re.sub('[-:_、【】。；：)(「」，.&+\n\t\r\u3000]', '', news_type))
            
            # 取發布日期
            news_date = soup.select('div[class=box_2]')[j].select('span[class=date]')[0].text.split()[2]
            News_Date.append(news_date)
            print(news_date)
            
            # 取發布時間
            news_time = soup.select('div[class=box_2]')[j].select('span[class=date]')[0].text.split()[3]
            News_Time.append(re.sub('[-_、【】。；：)(「」，.&+\n\t\r\u3000]', '', news_time))
#             print(re.sub('[-_、【】。；：)(「」，.&+\n\t\r\u3000]', '', news_time))
            
            # 取新聞內容
            page_res = requests.get(url=link, headers=headers)
            page_soap = BeautifulSoup(page_res.text, 'html.parser')

            for content in page_soap.select('div[class="story"]'):
                try:
                    News_Content.append(re.sub('[-:_、【】。；：)(「」，.&+\n\t\r\u3000]', ' ', content.text))
                except:
                    pass
            for content in page_soap.select('div[class="story lazyload"]'):
                try:
                    News_Content.append(re.sub('[-:_、【】。；：)(「」，.&+\n\t\r\u3000]', ' ', content.text))
                except:
                    pass
            
        except:
            pass
        
        sleep_time = random.randint(5,10)
        print("sleep time: %s sec"%(sleep_time))
        print('==========')
        time.sleep(sleep_time)
        
print("--- spend %s seconds ---" % (time.time() - start_time))
print('共爬取' + str(len(News_Title)) + '則新聞')



# 要存成 dataframe 的時候，發生爬取資料 array 不一樣的情形
# 用 len 去檢查後，發現 News_Content 的資料多了一筆
# 檢查後將同樣array的資料轉成df1
# News_Data = {'ID':News_ID, '標題':News_Title, '類型':News_Type, '網址':News_Link, '發布日期':News_Date, '發布時間':News_Time }
# df1 = pd.DataFrame(News_Data)

News_Data = {'ID':News_ID, '標題':News_Title, '類型':News_Type, '網址':News_Link, '發布日期':News_Date, '發布時間':News_Time, '內容':News_Content}
df_news_craw = pd.DataFrame(News_Data)

# 將多出一筆的資料存成df2
# df2 = pd.DataFrame({'內容':News_Content})

# 展開所有 row 方便進行交叉比對
# pd.set_option('display.max_rows', None)

# (人工手動)找到重複的部分為index=1372這筆資料，drop掉後重新整理index，並建立成新的dataframe命名為df3
# df3 = df2.drop(df.index[[1372]])
# df3.reset_index(inplace=True, drop=True)

# 將df1和df3用outer join的方式，合併成為需要的dataframe
# df_news_craw = df1.merge(df3, how='outer', left_index=True, right_index=True)

# 進行所需資料清洗，並建立最後要使用的dataframe
news_type1 = df_news_craw['類型'] == '生活'
news_type2 = df_news_craw['類型'] == '政治'
news_type3 = df_news_craw['類型'] == '地方'
news_type4 = df_news_craw['類型'] == '健康'
news_type5 = df_news_craw['類型'] == '財經'
news_type6 = df_news_craw['類型'] == '大陸'
news_type7 = df_news_craw['類型'] == '國際'
news_type8 = df_news_craw['類型'] == '論壇'
news_type9 = df_news_craw['類型'] == 'ETlife'
news_type10 = df_news_craw['類型'] == '其它'

df_banana_news = df_news_craw[(news_type1 | news_type2 | news_type3 | news_type4 | news_type5 | news_type6 | news_type7 | news_type8 | news_type9 | news_type10)]
# df_banana_news_etl.to_csv('東森新聞雲_香蕉.csv', index=False)
print(df_banana_news['標題'])



client = pymongo.MongoClient("mongodb+srv://<username>:<password>@<project_name>.i2omj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client.TWFruits
ettoday_news = db.ettoday_news_craw

print("ettoday_news update to mongodb -> start")

for excist_id in df_banana_news['ID']:
    if [x for x in ettoday_news.find({'ID':excist_id})] == []:
        ettoday_news_update = df_banana_news.loc[df_banana_news["ID"]==excist_id].to_dict(orient='records')
        updated = ettoday_news.insert_one(ettoday_news_update[0]).inserted_id
        print("ettoday_news update id", updated)
        
print("ettoday_news update to mongodb -> finish")
>>>>>>> 0d0be837c73068e4cfd50420f78ca45e1165a0b4
client.close()