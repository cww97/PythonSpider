# -*- coding:utf-8 -*-
import urllib.request
from bs4 import BeautifulSoup
import csv
import re
headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
f = open("web.html", "w")
csvfile = open('test2.csv', 'w+')
writer = csv.writer(csvfile)


def get_soup(weburl):
    req = urllib.request.Request(url=weburl, headers=headers)
    webPage=urllib.request.urlopen(req)
    data = webPage.read()
    soup = BeautifulSoup(data, 'lxml')
    return soup


def get_info(weburl):
    soup = get_soup(weburl)
    # f.write(soup.prettify())
    result = soup.find_all('ul', attrs= {"class": "parameter2 p-parameter-list"})
    if len(result) > 0:
        result = BeautifulSoup(str(result[0]), 'lxml').find_all('li')
    #print(soup.find_all('div', attrs={'class': "comment-content"}))
    ans = []
    for list in result:
        ans.append(str(list.string))
    writer.writerow(ans)


def getlist(weburl):
    soup = get_soup(weburl)
    f.write(soup.prettify())
    result = soup.find_all('div', attrs={"class": "gl-i-wrap"})
    pat = re.compile(r'href="([^"]*)"')
    ans = []
    i = 0
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
            print(link)
            path = 'pics//%s.jpg' % (i)
            urllib.request.urlretrieve(link, path)
        i += 1
        #print('i = %d\n' %  i )
    return ans


if __name__ == '__main__':
    url_list = 'https://search.jd.com/Search?keyword=dior&enc=utf-8&wq=dior&pvid=ee8a3e8f16794b6081b14a9773082c47'
    urls = getlist(url_list)
    for item in urls: get_info(item)