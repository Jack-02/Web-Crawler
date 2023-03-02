#巨潮网

import json
import requests
import re
from datetime import date


def collection(content: dict, sizelim: int, datelim: date, counter: int, destjson: list):
    '''巨潮网的信息提取方法'''

    data = content["announcements"]

    for item in data:
        if counter == sizelim:
            print("---Crawling finished due to data-size limitation!---")
            return -1
        title = re.sub('<.+?>', '', item['announcementTitle'])
        pdfurl = 'http://static.cninfo.com.cn/'+item['adjunctUrl']
        currentdatestr = re.findall('/.{10}/', item['adjunctUrl'])[0][1:-1]
        currentdate = date.fromisoformat(currentdatestr)
        if datelim > currentdate:
            print("---Crawling finished due to ending-date limitation!---")
            print(currentdate)
            return -1

        data = {'title': title, 'url': pdfurl,'publishdate': currentdatestr,'src':'cinfo'}
        destjson.append(data)
        counter += 1
        print(counter, data)
    return counter


def visit(destjson:list, stopdate: date):
    '''巨潮网网页爬取'''

    typedic = {'shj': 358, 'hke': 5559}
    for type in typedic:
        print('---------------------------------------')
        print(type)
        counter = 0
        pagenum = typedic[type]//10 if typedic[type] % 10 else typedic[type]//10 + 1
        page = 1
        while page <= pagenum:
            try:
                url = f"http://www.cninfo.com.cn/new/fulltextSearch/full?searchkey=%E7%8E%AF%E5%A2%83+%E7%A4%BE%E4%BC%9A%E5%8F%8A&sdate=&edate=&isfulltext=false&sortName=pubdate&sortType=desc&pageNum={page}&type={type}"

                headers = {
                    'Accept': 'application/json, text/javascript, */*; q=0.01',
                    'Accept-Encoding': 'gzip, deflate',
                    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                    'Connection': 'keep-alive',
                    'Cookie': 'JSESSIONID=8BEEB8E61FFD1A7726401029B3469D10; _sp_ses.2141=*; insert_cookie=37836164; routeId=.uc2; _sp_id.2141=7848bb9e-25a3-40aa-ad5d-8eeb593910fc.1677555240.1.1677555349.1677555240.0be633e9-ae78-4197-94f2-8d6a6025d818',
                    'Host': 'www.cninfo.com.cn',
                    'Referer': 'http://www.cninfo.com.cn/new/fulltextSearch?notautosubmit=&keyWord=%E7%A4%BE%E4%BC%9A%E8%B4%A3%E4%BB%BB%E6%8A%A5%E5%91%8A',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.57',
                    'X-Requested-With': 'XMLHttpRequest'
                }
                resp = requests.get(url, headers=headers)
                content = resp.json()
                counter = collection(content, typedic[type], stopdate, counter, destjson)
                if counter == -1:
                    break
                page += 1
            except BaseException as e:
                print('远程主机强迫关闭了一个现有的连接。但是没关系，本页重来！')
