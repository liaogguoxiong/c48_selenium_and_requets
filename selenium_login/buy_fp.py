#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time             : 2019-10-22 9:34
# @Author           : lgx
# @project_name     : c48_selenium_and_requets
# @File             : buy_fp.py
# @Des: 购买发票

from  deal_input_file import get_info
import requests
from bs4 import BeautifulSoup as BS
from dzfp_c48 import *
import requests.exceptions


def buy():

    company_info=get_info()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}


    s=input("输入申领发票的税号:")
    for i in company_info:
        for j in company_info[i]:
            # print(j)
            if s in j:
                ipp=i
                shuihao=j[0]
                fjh=j[1]

    # print(ipp,shuihao,fjh)
    cs=c48_sys(ipp)
    cs.login_c48()
    cookies = cs.get_cookie()
    cs.close_browse()
    cookie = {}
    for c in cookies:
        cookie[c['name']] = c['value']
    print(cookie)
    req_url="http://{}/zzs_kpfw_manager/invoice/purchase/list.htm".format(ipp)
    r1=requests.get(req_url,headers=headers,cookies=cookie)
    # print(r1.cookies)
    pycx_url = "http://{ipp}/zzs_kpfw_manager/invoice/purchase/pycx.htm?nsrxxStr={shuihao},{fjh},,{shuihao},{fjh},{fjh},51,end&totalRows=1".format(ipp=ipp,shuihao=shuihao,fjh=fjh) # 票源查询的url
    n=0
    while n < 3:
        try:
            res=requests.get(pycx_url,headers=headers,cookies=cookie,timeout=20)
            soup=BS(res.text,"lxml")
            table=soup.find_all(class_="commonTableNew")
            td=table[0].find_all("td")
            fp_num=td[1].text
            fp_num=fp_num.replace("份","")
            if fp_num == "":
                print("局端没有可以下载票源")
                n+=1
            else:
                print("局端的票源份数:", fp_num)
                fplg_url="http://{ipp}/zzs_kpfw_manager/invoice/purchase/wslp.htm?nsrxxStr={shuihao},{fjh},{fp_num},{shuihao},{fjh},{fjh},51,end&totalRows=1".format(ipp=ipp,shuihao=shuihao,fjh=fjh,fp_num=fp_num)
                r2=requests.get(fplg_url,headers=headers,cookies=cookie,timeout=20)
                print("下载成功")
        except requests.exceptions.ReadTimeout:
            print("请求超时")
            n+=1


buy()