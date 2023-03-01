import json
import requests
import re
from datetime import date
import argparse

import cinfo
import shse
import szse

def get_order():
    '''Get order from user and return args.'''
    parser = argparse.ArgumentParser(
        description='Get order including datasource, date, downloadpath(of a json file)')
    parser.add_argument('--src', '-s', help='''The source website 1:cinfo(巨潮网), 2: shse(上交所), 3:szse(深交所), 0:all above. 
    Input the number before colon. Default 0''', type=int, default=0)
    parser.add_argument('--date', '-d', help='''Update the reports in the time frame from now to the assigned date. Example: 2021-01-23. Defalt update all''')
    parser.add_argument(
        '--path', '-p', help='The json file download path. Required!', required=True)
    args = parser.parse_args()
    return args


def main():
    arg=get_order()
    src,stopdatestr,path=arg.src,arg.date,arg.path
    if stopdatestr==None:
        stopdate=date.min
    else:
        stopdate=date.fromisoformat(stopdatestr)
    totaldata=[]
    if src==1:
        cinfo.visit(totaldata,stopdate)
    elif src==2:
        shse.visit(totaldata,stopdate)
    elif src==3:
        szse.visit(totaldata,stopdate)
    elif src==0:
        cinfo.visit(totaldata,stopdate)
        shse.visit(totaldata,stopdate)
        szse.visit(totaldata,stopdate)

    else:
        print('WRONG INPUT!!')
        return 
   
    # with open(path,'w+',encoding='utf-8') as f :
    with open(f'../totaldata.json','w+',encoding='utf-8') as f :
        json.dump(totaldata,f,ensure_ascii=False)

if __name__=='__main__':
    main()
    