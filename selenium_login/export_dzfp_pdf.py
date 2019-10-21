#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time             : 2019-10-20 13:45
# @Author           : lgx
# @project_name     : c48_selenium_and_requets
# @File             : export_dzfp_pdf.py
# @Des: 调出电子发票的月度汇总pdf

from  deal_input_file import get_info
import requests
import datetime
from dzfp_c48 import *

def export_pdf():
    company_info = get_info()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
    year=datetime.datetime.now().year
    month=datetime.datetime.now().month-1
    if month < 10:
        month="0"+str(month)
    for ipp in company_info:
        cs = c48_sys(ipp)
        cs.login_c48()
        cookies=cs.get_cookie()
        cs.close_browse()
        cookie={}
        for c in cookies:
            cookie[c['name']]=c['value']
        for i in company_info[ipp]:
            company_name = i[2]
            shuihao = i[0]
            fjh=i[1]
            url="http://{ipp}/zzs_kpfw_manager/tax/monthly_statistics/doExportPdf.htm?nsrsbh={shuihao}&cardno={fjh}&year={year}&month={month}&fpzl=51".format(ipp=ipp,shuihao=shuihao,fjh=fjh,year=year,month=month)
            pdf_path="C:/Users/lgx/Downloads/{}.pdf".format(company_name)
            res=requests.get(url,headers=headers,cookies=cookie)
            with open(pdf_path,"wb") as f:
                f.write(res.content)
            print("{}pdf导出完毕!!!!".format(company_name))


export_pdf()