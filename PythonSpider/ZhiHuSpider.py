import requests
import time
import json
import importlib
import os
import re

from bs4 import BeautifulSoup
from PIL import Image




'''
知乎爬虫工作流程：

1. 使用账号密码，获取并人工输入验证码，调用login_with_email_pwd登陆并创建cookies
2. 使用登陆后的session进行推各种操作

'''

Default_Header = {'X-Requested-With': 'XMLHttpRequest',
                  'Referer': 'http://www.zhihu.com',
                  'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; '
                                'rv:39.0) Gecko/20100101 Firefox/39.0',
                  'Host': 'www.zhihu.com'}

Zhihu_URL = 'http://www.zhihu.com'
Login_URL = Zhihu_URL + '/login/email'
Captcha_URL_Prefix = Zhihu_URL + '/captcha.gif?r='
Cookies_File_Name = 'cookies.json'

global session
session = requests.Session()

def get_captcha():
    #获取验证码数据。
    #Captcha_URL_Prefix + str(int(time.time() * 1000)) 这个生成的是验证码的网址！
    r = session.get(Captcha_URL_Prefix + str(int(time.time() * 1000)))
    return r.content


def login_with_email_pwd(email='', password=''):

    print('====== zhihu login =====')

    captcha_data = get_captcha()
    with open('captcha.gif', 'wb') as f:
        f.write(captcha_data)

    print('please check captcha.gif for captcha')
    #image=Image.open('captcha.gif')
    #image.show()
    captcha = input('captcha: ')
    os.remove('captcha.gif')

    print('====== logging.... =====')

    data = {'email': email, 'password': password,
            'remember_me': 'true', 'captcha': captcha}
    r = session.post(Login_URL, data=data)
    j = r.json()
    code = int(j['r'])
    message = j['msg']
    cookies_str = json.dumps(session.cookies.get_dict()) \
        if code == 0 else ''

    if code == 0:
        print('login successfully')
    else:
        print('login failed, reason: {0}'.format(message))

    if cookies_str:
        with open(Cookies_File_Name, 'w') as f:
            f.write(cookies_str)
        print('cookies file created.')
    else:
        print('can\'t create cookies.')


def login_with_cookies(cookies):
    #使用cookies文件或字符串登录知乎
    with open(cookies) as f:
        cookies = f.read()
    cookies_dict = json.loads(cookies)
    session.cookies.update(cookies_dict)

def login_zhihu():
    if os.path.isfile(Cookies_File_Name):
        login_with_cookies(Cookies_File_Name)
    else:
        login_with_email_pwd('xxx@qq.com','pwd')



target_url='http://www.zhihu.com/topic/19584431/top-answers?page='
page_num=1
question_links=[]
login_zhihu()

#至此,便已完成了登陆，login_zhihu函数会判断是否已经有了cookies，若没有则创建。
#接下来就能用全局变量session会话进行各种操作了！

cur_url='http://www.zhihu.com/topic/19584431/top-answers?page='+str(page_num)
html=session.get(cur_url)

while(html.status_code==200):
    html.encoding='utf-8'
    soup = BeautifulSoup(html.text,'lxml')
    links = soup.find_all('a')
    for link in links:
        if(link.get('class')==['question_link']):
            print(Zhihu_URL+link['href'])
            question_links.append(Zhihu_URL+link['href'])
    page_num+=1
    print('---------------'+str(page_num)+'-------------')
    cur_url='http://www.zhihu.com/topic/19584431/top-answers?page='+str(page_num)
    html=session.get(cur_url)

fileNameHead='zhihu/zhihu_img'
count=0

for link in question_links:
    response = session.get(link)
    response.encoding = 'utf-8'
    content = response.text
    soup = BeautifulSoup(content,'lxml')
    imgBox = soup.find_all('img')
    for img in imgBox:
        matchObj = re.match( r'(.*?\.jpg)', img['src'])
        if matchObj:
            try:
                r = requests.get('http:'+img['src'],timeout=5)
                if(r.status_code==200):
                    fileName = fileNameHead + str(count) + '.jpg'
                    with open(fileName, "wb") as imgFile:
                        print(img['src'] + '  is downloading!')
                        imgFile.write(r.content)
                    count+=1
                if count>10:
                    break
            except requests.exceptions.RequestException:
                print('except')
                count+=1
