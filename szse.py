#深圳证券交易所

import requests
import re
from datetime import date
import time
from tqdm import tqdm

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
            return -1
        data = {'title': title, 'url': pdfurl,'publishdate': currentdatestr,'src':'szse'}
        destjson.append(data)
        counter += 1
    return counter


def visit(destjson: list, stopdate: date):
    '''深交所网页爬取'''
    maxnum=120
    pagenum=6
    page=1
    counter=0
    errortimes=0
    pbar = tqdm(total=pagenum,desc=f"深交所官网")
    while page<=pagenum:
        try:
            #冷却1秒
            time.sleep(1)

            #开始请求
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

            #信息处理
            content=requests.post(url, headers=headers).json()
            counter = collection(content, maxnum, stopdate, counter, destjson)

            #达到要求，退出
            if counter == -1:
                pbar.close
                break

            page+=1
            pbar.update(1)
            errortimes=0

        except KeyboardInterrupt:
            print("您已终止深交所爬取")
            pbar.close
            return
        
        except BaseException as e:
            #请求失败
            errortimes+=1
        
        #同页请求多次出错，跳过
        if errortimes==10:
            page+=1
            errortimes=0
    pbar.close
        
