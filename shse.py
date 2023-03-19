#上海证券交易所

import json
import requests
import re
from datetime import date
import time
from tqdm import tqdm

def collection(content: dict, sizelim: int, datelim: date, counter: int, destjson: list):
    '''上交所的信息提取方法'''

    data = content["data"]
    for item in data:
        if counter == sizelim:
            print("---Crawling finished due to data-size limitation!---")
            return -1
        
        title = item['CTITLE_TXT']
        pdfurl = 'http://www.sse.com.cn'+item['CURL']
        currentdatestr = item['CRELEASETIME']
        currentdate = date.fromisoformat(currentdatestr)
        if datelim > currentdate:
            print("---Crawling finished due to ending-date limitation!---")
            return -1
        data = {'title': title, 'url': pdfurl,'publishdate': currentdatestr,'src':'shse'}
        destjson.append(data)
        counter += 1
    return counter


def visit(destjson: list, stopdate: date):
    '''上交所网页爬取'''

    maxnum=217
    pagenum=22
    page=1
    counter=0
    errortimes=0
    pbar = tqdm(total=pagenum,desc=f"上交所官网")
    while page<=pagenum:
        try:
            #冷却1秒
            time.sleep(1)

            #开始请求
            url = f'http://query.sse.com.cn/search/getSearchResult.do?search=qwjs&jsonCallBack=jsonpCallback89910378&searchword=T_L+CTITLE+T_E+T_L%E7%8E%AF%E5%A2%83%E3%80%81%E7%A4%BE%E4%BC%9A%E5%8F%8A+T_R+and+cchannelcode+T_E+T_L0T_D8311T_D8348T_D8349T_D8365T_D9856T_D9860T_D9862T_D12002T_D88888888T_RT_R&orderby=-CRELEASETIME&page={page}&perpage=10&_=1677475917888'
            headers = {
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate',
                'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
                'Connection': 'keep-alive',
                'Cookie': 'ba17301551dcbaf9_gdp_user_key=; gdp_user_id=gioenc-ae5184d3%2C11d0%2C5c12%2Caaad%2C3dc118g2ad20; ba17301551dcbaf9_gdp_session_id_a14d4c06-55c3-4acc-874c-08c1c6948e41=true; yfx_c_g_u_id_10000042=_ck23022623101610860367501513895; ba17301551dcbaf9_gdp_session_id_f96ec840-927d-43ce-9f51-0f265db95987=true; ba17301551dcbaf9_gdp_session_id_e4109ad7-c8de-4354-a5d7-b7e244ec0f5d=true; ba17301551dcbaf9_gdp_session_id_934db1b1-8451-49cf-ba3f-f23be3ec2c25=true; ba17301551dcbaf9_gdp_session_id_347a1467-41be-436c-ae61-41caf6ad07b4=true; ba17301551dcbaf9_gdp_session_id_4911142e-3a14-4e90-bd79-63a93352b5cd=true; yfx_f_l_v_t_10000042=f_t_1677424214629__r_t_1677635683201__v_t_1677636029714__r_c_3; ba17301551dcbaf9_gdp_session_id=2344714f-722d-4ce9-be8a-bc159265a982; ba17301551dcbaf9_gdp_session_id_2344714f-722d-4ce9-be8a-bc159265a982=true; ba17301551dcbaf9_gdp_sequence_ids={%22globalKey%22:146%2C%22VISIT%22:8%2C%22PAGE%22:17%2C%22VIEW_CLICK%22:84%2C%22VIEW_CHANGE%22:15%2C%22CUSTOM%22:26}',
                'Host': 'query.sse.com.cn',
                    'Referer': 'http://www.sse.com.cn/',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.57'
            }
            resp = requests.get(url=url, headers=headers)
            jsonpcb = resp.text

            #将jsonpCallback转为json
            filter = re.findall("(jsonpCallback.*?\().+", jsonpcb)[0]
            content = json.loads(jsonpcb[len(filter):-1])

            #信息处理
            counter = collection(content, maxnum, stopdate, counter, destjson)

            #达到要求，退出
            if counter == -1:
                pbar.close
                break

            page += 1 
            pbar.update(1)
            errortimes=0
        
        except KeyboardInterrupt:
            print("您已终止上交所爬取")
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
        
