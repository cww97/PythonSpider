import urllib.request
from bs4 import BeautifulSoup

webheader = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
    #'Accept-Encoding': 'gzip, deflate',
    'Host': 'www.douban.com',
    'DNT': '1'
    }

def get_comments(weburl):
    req = urllib.request.Request(url=weburl, headers=webheader)
    webPage=urllib.request.urlopen(req)
    data = webPage.read()
    data = data.decode('UTF-8')
    soup = BeautifulSoup(data,"lxml")
    for list in soup.find_all('span', attrs={"class": "a-size-base review-text"}):
        st = list.string
        if st != None and st[0] != 'гд':
            f.write(st)
            f.write("\n")

f = open("result.txt", "w")#get comments of one childrenbike
f.write("""
==============================
by cww97
here is the children bike
https://www.amazon.cn/%E5%AD%A9%E5%AD%90%E5%AE%B6%E4%B8%89%E8%BD%AE%E8%BD%A6%E5%84%BF%E7%AB%A5%E7%94%B5%E5%8A%A8%E6%91%A9%E6%89%98%E8%BD%A6-%E5%84%BF%E7%AB%A5%E7%94%B5%E5%8A%A8%E8%BD%A6-%E7%AB%A5%E8%BD%A6%E7%8E%A9%E5%85%B7%E8%BD%A6%E5%84%BF%E7%AB%A5%E5%8F%AF%E5%9D%90/dp/B00DQGTK4W/ref=sr_1_2?ie=UTF8&qid=1464775734&sr=8-2&keywords=%E7%AB%A5%E8%BD%A6" \

===============================
""")

for i in range(6):
    url = "https://www.amazon.cn/product-reviews/B00DQGTK4W/ref=cm_cr_dp_see_all_summary?ie=UTF8&showViewpoints=%d&sortBy=helpful"%(i+1)
    get_comments(url)
