#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time             : 2019-10-24 11:32
# @Author           : lgx
# @project_name     : c48_selenium_and_requets
# @File             : sync_info.py
# @Des:

from  deal_input_file import get_info
import requests
from bs4 import BeautifulSoup as BS
from dzfp_c48 import *
import requests.exceptions
import re

def nsr_info():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"
    }
    company_info=get_info()
    for ipp in company_info:
        cs=c48_sys(ipp)
        cs.login_c48()
        cookies=cs.get_cookie()
        cs.close_browse()
        cookie={}
        for c in cookies:
            cookie[c['name']]=c['value']

        req_url="http://{}/zzs_kpfw_manager/init/nsr_info/list.htm".format(ipp)
        no_update={}
        d_error={}
        for i in company_info[ipp]:
            shuihao=i[0]
            fjh=i[1]
            name=i[2]
            form_data={

                "search_nsrmc":name,
                "search_nsrsbh":shuihao,
                "search_fjh":fjh
            }
            print("查询的是:",name)
            res=requests.post(req_url,headers=headers,data=form_data,cookies=cookie)
            try:
                soup=BS(res.text,"lxml")
                a=soup.find_all('a')
                str=a[2]['href']
                num=re.search("\d+",str).group()
                # print(num)

                sync_url="http://{}/zzs_kpfw_manager/init/nsr_info/synchroStatus/{}.htm".format(ipp,num)
                query_url="http://{}/zzs_kpfw_manager/init/nsr_info/taxInfoDetail/{}.htm".format(ipp,num)

                r1=requests.get(query_url,headers=headers,cookies=cookie)

                tr=BS(r1.text,'lxml').find_all("tr")
                td=tr[3].find_all('td')
                no_line_time=td[7].text
                no_line_money=td[8].text
                odd_money=td[9].text

                print("离线时间:",no_line_time)
                print("离线金额:",no_line_money)
                print("剩余离线时间:",odd_money)

                if int(no_line_time) < 168:
                    no_update[name]=no_line_time
                    try:
                        r2=requests.get(sync_url,headers=headers,cookies=cookie,timeout=20)
                        print("同步成功")
                    except requests.exceptions.ReadTimeout:
                        d_error[shuihao] = name

            except IndexError:
                d_error[shuihao]=name
                continue

    print(no_update)
    print(d_error)


nsr_info()