#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time             : 2019-10-22 13:35
# @Author           : lgx
# @project_name     : c48_selenium_and_requets
# @File             : select_fp.py
# @Des: 查询发票,也就是导出发票

from  deal_input_file import get_info
import requests
from dzfp_c48 import *
import requests.exceptions
from datetime import datetime
import os

def export_fp():
    year=datetime.now().year
    month=datetime.now().month-1
    company_info = get_info()
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}

    for ipp in company_info:
        req_url="http://{}/zzs_kpfw_manager/invoice/query/exportAll.htm".format(ipp)
        cs=c48_sys(ipp)
        cs.login_c48()
        cookies=cs.get_cookie()
        cookie={}
        for c in cookies:
            cookie[c['name']]=c['value']
        print(cookie)
        for i in company_info[ipp]:
            shuihao=i[0]
            fjh=i[1]
            company_name=i[2]
            if len(i) == 4:
                path = "D:/发票明细/{}月/其他".format(month)
            else:
                path = "D:/发票明细/{}月/捷顺".format(month)
            if not os.path.exists(path):
                    os.makedirs(path)
            data2={
                    "export_nsrsbh": shuihao,
                    "export_cardno":fjh ,
                    "export_fpdm": "",
                    "export_fphm": "",
                    "export_upload_status": "",
                    "export_kprq_start": "{year}-{month}-01 00:00:00".format(year=year,month=month),
                    "export_kprq_end": "{year}-{month}-31 23:59:59".format(year=year,month=month),
                    "export_kplx": "",
                    "export_serial_num": "",
            }
            r2=requests.post(req_url,headers=headers,data=data2,cookies=cookie)


            fp_file=path+"/{}.xlsx".format(company_name)
            with open(fp_file,"wb") as f:
                f.write(r2.content)

            print("{}导出完毕".format(company_name))


export_fp()