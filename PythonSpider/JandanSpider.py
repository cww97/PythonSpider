from bs4 import BeautifulSoup
import requests
import re

try:
    hearderData = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2438.3 Safari/537.36',
        'HTTPS': '1',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
        'Cookie': '4157036015=28; _gat=1; gif-click-load=off; 4157036015=12; _ga=GA1.2.1428244724.1439731704; ',
    }

    origin_url = 'http://jandan.net/ooxx/page-'
    origin_page = 953
    count = 0
    fileNameHead = 'D:\jandan\jandan\jandan'

    session = requests.Session()
    response = session.get(origin_url + str(origin_page),headers=hearderData)
    while(response.status_code==200):
        try:
            print('\n--------------------\n'+str(origin_page)+'\n-------------------\n')
            response = session.get(origin_url + str(origin_page),headers=hearderData)
            response.encoding = 'utf-8'
            html = response.text
            soup = BeautifulSoup(html,'lxml')
            imgBox = soup.find_all('img')
            for img in imgBox:
                matchObj = re.match( r'(.*?\.jpg)', img['src'])
                if matchObj:
                    r = requests.get(img['src'],timeout=5)
                    print(r.status_code)
                    if(r.status_code==200):
                        fileName = fileNameHead + str(count) + '.jpg'
                        with open(fileName, "wb") as imgFile:
                            print(img['src'] + '  is downloading!')
                            imgFile.write(r.content)
                        count+=1
            origin_page+=1
        except requests.exceptions.RequestException:
            print('RequestException')
            count+=1
            origin_page+=1
finally:
    print('Exception')