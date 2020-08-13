'''
@Author: Charon
@Date: 2020-04-04 12:42:45
@LastEditTime: 2020-04-05 21:55:49
'''
#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import re
import os
import time
from bs4 import BeautifulSoup as bs


# In[2]:


headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36', 'cookie': '__cfduid=dbc4a25090b9c655e91440677115e64251585898884; _ga=GA1.2.2122477128.1585898921; _gid=GA1.2.1379899880.1585898921; sc_is_visitor_unique=rx11860127.1585918213.04A600EC165D4F38E07A021EBE303A26.5.3.3.2.2.2.2.2.2'
           }


# In[3]:

def scrap(root, key):
    htmls = []
    judge = True
    i = 1
    url = root+'/?s='+str(key)
    while judge:
        judges = []
        req = requests.get(url, headers=headers)
        soup = bs(req.text, 'lxml')
        xx = soup.find_all(attrs={'rel': 'nofollow', 'class': 'inactive'})
        for x in xx:
            judges.append(x.string)
        if str(i+1) in judges:
            url = root+'/page/'+str(i+1)+'/?s='+str(key)
            i += 1
        else:
            judge = False
        htmls.append(req.text)

    # In[4]:
    pichtmls = []
    for html in htmls:
        soup = bs(html, 'lxml')
        a = soup.find_all(
            attrs={'rel': 'nofollow', 'id': 'featured-thumbnail'})
        # print(a)
        for i in a:
            pichtml = i.get('href')
    #         print(pichtml)
            pichtmls.append(pichtml)
    print(pichtmls)

    errornum = 0
    # In[5]:
    picurls = []
    for h in pichtmls:
        try:
            r1 = requests.get(h, headers=headers, timeout=5).text
            soup1 = bs(r1, 'lxml')
            span = soup1.find_all(class_='blue')
        #     print(span)
            picurl = span[0].get('href')
            print(picurl)
            picurls.append(picurl)
        except:
            print('error')
            errornum += 1
    # print(picurls)
    n = 0
    for pic in picurls:
        time.sleep(1)
        dir_name = key
        if not os.path.exists(dir_name):  # 创建文件夹
            os.mkdir(dir_name)
        fname = pic.split('/')[-1].split('_')[-1].split('&')[0]
        try:
            response = requests.get(pic, headers=headers, timeout=5)
            with open(dir_name + '/' + fname, 'wb') as f:  # 写入文件
                f.write(response.content)
                print(pic)
                print('downloading:', fname)
                n = n+1
        except:
            print('error')
            errornum += 1
    print('Download successfully,Total:', n)
    print('Errors:', errornum)


def main():
    print('Please input the keyword to search:')
    keyw = input()
    root = 'https://www.pixel4k.com'
    scrap(root, keyw)


if __name__ == '__main__':
    main()
