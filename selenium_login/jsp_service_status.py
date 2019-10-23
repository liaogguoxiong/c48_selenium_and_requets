#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time             : 2019-10-19 14:51
# @Author           : lgx
# @project_name     : c48_selenium_and_requets
# @File             : jsp_service_status.py
# @Des: 检查金税设备的服务状态

from  deal_input_file import get_info
import requests
from bs4 import BeautifulSoup as BS
from dzfp_c48 import *




def get_status():

    company_info=get_info()
    print(company_info)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}

    for ipp in company_info:
        req_url = "http://{}/zzs_kpfw_manager/statistic/queryServiceData.htm".format(ipp)
        cs = c48_sys(ipp)
        cs.login_c48()
        cookies=cs.get_cookie()
        cs.close_browse()
        cookie={}
        for c in cookies:
            cookie[c['name']]=c['value']
        print(cookie)
        wrong_status={}
        for i in company_info[ipp]:
            company_name=i[2]
            shuihao=i[0]
            data = {
                "search_nsrmc": company_name,
                "search_nsrsbh": shuihao
            }
            res = requests.post(req_url, headers=headers, cookies=cookie, data=data)
            # print(res.status_code)
            soup = BS(res.text, 'lxml')
            # print(soup)
            tbody = soup.find_all("tbody")[0]
            status = tbody.find_all("span")[0].text
            print("{}的状态是:{}".format(company_name, status))
            if status != "可用":
                wrong_status[company_name]=status

    print(wrong_status)


get_status()