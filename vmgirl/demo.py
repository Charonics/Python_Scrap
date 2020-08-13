'''
@Author: Charon
@Date: 2020-04-06 18:16:45
@LastEditTime: 2020-04-07 13:01:31
'''
# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %% [markdown]
# requests+正则表达式抓取需要翻页网站套图

# %%
import requests
import re
import os
import time
from lxml import etree
'''请求网页'''
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36 Edg/80.0.361.62','referer': 'https://www.vmgirls.com/pure'}

# %%
resqs=[]
for page in range(5):  #Ajax异步加载请求
    ur = 'https://www.vmgirls.com/wp-admin/admin-ajax.php'
    param = {
        'append': 'list-archive',
        'paged': page+1,
        'action': 'ajax_load_posts',
        'query': '18',
        'page': 'cat'
    }
    resq = requests.post(url=ur, data=param, headers=headers)
    resqs.append(resq.text)
urls=[]
for res in resqs:
    resq_tree = etree.HTML(res)
    urls.extend(resq_tree.xpath('//a[@class="media-content"]//@href'))  # 获取每篇文章的链接


# %%
htmls = []
for url in urls:
    judge = True
    i = 1
    baseurl = url.split('//')[0]+'//'+url.split('//')[1].split('/')[0]+'/'
    while judge:
        judges = []
        r = requests.get(url, headers=headers)
        r_tree = etree.HTML(r.content)
        judges = r_tree.xpath(
            '//a[@class="post-page-numbers"]/text()')  # 获取下一页信息得到一个列表
        if str(i + 1) in judges:  # 实现动态判断并加载下一页
            if i == 1:
                url = baseurl + url.split('/')[-1].split('.')[0] + '/page-' + str(i + 1) + '.html'
            else:
                url = baseurl + url.split('/')[-2]+'/page-'+str(i+1)+'.html'
            i += 1
        else:
            judge = False
        htmls.append(r.text)


# %%
for html in htmls:
    '''设置保存位置'''
    # print(html)
    dir_name = re.findall('<h1 class="post-title h3">(.*?)</h1>', html)[-1]
    print(dir_name)
    if not os.path.exists(dir_name):  # 创建文件夹
        os.mkdir(dir_name)
    picurls = re.findall('<a href="(.*?)" alt=".*?" title=".*?">', html)
    # print(urls)

    '''保存图片'''
    for picurl in picurls:
        time.sleep(1)
        fname = picurl.split('/')[-1]
        response = requests.get(picurl, headers=headers)
        print(picurl)
        with open(dir_name + '/' + fname, 'wb') as f:  # 写入文件
            f.write(response.content)
            print('Downloading Image:', fname)
print('Download Successfully')


# %%
import requests
headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.122 Safari/537.36 Edg/80.0.361.62','referer': 'https://www.vmgirls.com/pure'
}
for page in range(5):  #Ajax异步加载请求
    ur = 'https://www.vmgirls.com/wp-admin/admin-ajax.php'
    param = {
        'append': 'list-archive',
        'paged': page+1,
        'action': 'ajax_load_posts',
        'query': '18',
        'page': 'cat'
    }
    resp = requests.post(url=ur, data=param, headers=headers)
    print(resp.text)



# %%
