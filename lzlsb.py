# -*- coding:utf-8 -*-
import urllib.request
from urllib.parse import quote
from bs4 import BeautifulSoup
import csv
import re

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
f = open("web.html", "w")
csvfile = open('csv_test.csv', 'w+')
writer = csv.writer(csvfile)
comment_file = open('comments.csv','w+')
comment_writer = csv.writer(comment_file)


def get_soup(weburl):
    print(weburl)
    req = urllib.request.Request(url=weburl, headers=headers)
    #print(req)
    webPage=urllib.request.urlopen(req)
    data = webPage.read()
    soup = BeautifulSoup(data,'lxml')
    #f.write(soup.prettify())
    return soup


# 获取单个商品信息
def get_info(weburl):

    # 如果这是一个广告
    if str(weburl).__contains__('ccc-x'):
        writer.writerow('')
        comment_writer.writerow('')
        return

    soup = get_soup(weburl)
    result = soup.find_all('ul', attrs= {"class": "parameter2 p-parameter-list"})
    if len(result) > 0:
        result = BeautifulSoup(str(result[0]), 'lxml').find_all('li')

    # 商品基本信息
    info = []
    for item in result:
        info.append(str(item.string))
    writer.writerow(info)

    # 获取评论
    comments = []
    result = soup.find_all('div', attrs={"class": "comment-content"})
    for comment in result:
        comments.append(str(comment.string).replace('\n','，'))
    comment_writer.writerow(comments)


# 获取一个搜索页的商品列表

global top
def getlist(weburl):
    global top
    soup = get_soup(weburl)
    f.write(soup.prettify())
    result = soup.find_all('div', attrs={"class": "gl-i-wrap"})
    pat = re.compile(r'href="([^"]*)"')
    ans = []
    for item in result:
        # info
        product = BeautifulSoup(str(item),'lxml')
        url = product.find_all("div",attrs={"class":"p-name p-name-type-2"})
        url = BeautifulSoup(str(url), 'lxml').find_all('a')
        url = 'http:' + pat.search(str(url)).group(1)
        ans.append(url)

        # img
        img = product.find('img',attrs={"class": "err-product"})
        link = str(img.get('src'))
        if link == 'None':
            link = str(img.get('data-lazy-img'))
        if link != 'None':
            link = 'http:' + link
            #print(link)
            path = 'pics//%s.jpg' % (top)
            urllib.request.urlretrieve(link, path)
        top += 1
    print(top)
    return ans


def main():
    urls = []
    global top
    top = 0
    for i in range(30):
        url_list2 = 'https://search.jd.com/search?keyword='+quote('口红')+'&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&suggest=1.his.0.0&stock=1&ev=exbrand_'+quote('迪奥（Dior）')+'%7C%7C'+quote('纪梵希（Givenchy）')+'%7C%7C'+quote('香奈儿（Chanel）')+'%7C%7C'+quote('阿玛尼（ARMANI）')+'%7C%7C'+quote('兰蔻（LANCOME）')+'%7C%7C'+quote('娇兰（Guerlain）')+'%7C%7C'+quote('魅可（M.A.C）')+'%7C%7C'+quote('雅诗兰黛（Estee%20Lauder）')+'%7C%7CNARS%7C%7C'+quote('兰芝（LANEIGE）')+'%7C%7C'+quote('汤姆.福特（TOM%20FORD）')+ '%40&' + 'stock=1&page=%s&s=1&click=0'%i
        urls += getlist(url_list2)
    for item in urls: get_info(item)


if __name__ == '__main__':
    main()
