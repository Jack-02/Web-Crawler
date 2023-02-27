#来源：上海证券交易所中的社会责任报告：http://www.sse.com.cn/home/search/?webswd=%E7%A4%BE%E4%BC%9A%E8%B4%A3%E4%BB%BB%E6%8A%A5%E5%91%8A
#该简单初代版本仅用于获取报告pdf的网址，数据库确定后可以据此直接下载。
#预计共有5120篇报告

import json
import requests
import re


for page in range(1,4): #page共有512页，此处可更改
    url=f'http://query.sse.com.cn/search/getSearchResult.do?search=qwjs&jsonCallBack=jsonpCallback76339515&searchword=T_L+CTITLE+T_E+T_L%E7%A4%BE%E4%BC%9A%E8%B4%A3%E4%BB%BB%E6%8A%A5%E5%91%8A+T_R+and+cchannelcode+T_E+T_L0T_D8311T_D8348T_D8349T_D8703T_D8862T_D8874T_D8875T_D8879T_D8883T_D11348T_D11360T_D12002T_D88888888T_RT_R&orderby=-CRELEASETIME&page={page}&perpage=10&_=1677475917888'
    
    # 本人使用 fake_useragent 库出现未知错误，暂时未使用模拟代理。后续大批量爬取可能会被网站拦截。
    response=requests.get(
        url=url,
        headers={'Referer':'http://www.sse.com.cn/'}
    )
    jsonp_str = response.text

    #将jsonpCallback转为json
    filter = re.findall("(jsonpCallback.*?\().+",jsonp_str)[0]
    json_str=jsonp_str[len(filter):-1]
    data=json.loads(json_str)["data"]

    print(f'in page {page}:')
    for i in range(10):
        title=data[i]['CTITLE_TXT']
        pdfurl='http://www.sse.com.cn'+data[i]['CURL']
        print(title,pdfurl)
