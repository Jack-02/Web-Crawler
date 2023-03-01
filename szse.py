#深圳证券交易所

import json
import requests
import re
from datetime import date


def collection(content: dict, sizelim: int, datelim: date, counter: int, destjson: list):
    '''深交所的信息提取方法'''

    data = content["data"]
    for item in data:
        if counter == sizelim:
            print("---Crawling finished due to data-size limitation!---")
            return -1
        title = re.sub('<.+?>', '', item['doctitle'])
        rawurl=item['docpuburl']
        pdfurl = re.sub('download/','',rawurl)
        currentdatestr = re.findall('/.{10}/',rawurl)[0][1:-1]
        currentdate = date.fromisoformat(currentdatestr)
        if datelim > currentdate:
            print("---Crawling finished due to ending-date limitation!---")
            print(currentdate)
            return -1
        data = {'title': title, 'url': pdfurl,'publishdate': currentdatestr,'src':'szse'}
        destjson.append(data)
        counter += 1
        print(counter, data)
    return counter


def visit(destjson: list, stopdate: date):
    '''深交所网页爬取'''
    maxnum=120
    page=1
    counter=0
    while page<=6:
        try:
            url = f'http://www.szse.cn/api/search/content?SHOWTYPE=JSON&keyword=%E7%8E%AF%E5%A2%83%E3%80%81%E7%A4%BE%E4%BC%9A%E5%8F%8A&range=title&time=1&orderby=time&currentPage={page}&pageSize=20&openChange=true&searchtype=0&r=1677635581381'
            headers = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Connection': 'keep-alive',
                'Content-Type': 'application/json',
                'HOST': 'www.szse.cn',
                'Origin': 'http://www.szse.cn',
                'Referer': 'http://www.szse.cn/application/search/index.html?keyword=%E7%8E%AF%E5%A2%83%E3%80%81%E7%A4%BE%E4%BC%9A&r=1677635581381',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari1/537.36 Edg/110.0.1587.57',
                'X-Request-Type': 'ajax',
                'X-Requested-With': 'XMLHttpRequest'
            }

            content=requests.post(url, headers=headers).json()
            counter = collection(content, maxnum, stopdate, counter, destjson)
            if counter == -1:
                break
            page+=1
        except BaseException as e:
            print('远程主机强迫关闭了一个现有的连接。但是没关系，本页重来！')

        