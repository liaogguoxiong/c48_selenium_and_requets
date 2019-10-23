#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time             : 2019-10-20 12:53
# @Author           : lgx
# @project_name     : c48_selenium_and_requets
# @File             : deal_input_file.py
# @Des: 用于处理输入文件

import re

def get_info():
    with open("jieshun",'r',encoding="utf-8") as f:
        res1=f.readlines()

    # print(res1)
    res=[]
    for i in res1:
        if i != "\n":
            res.append(i)

    # print(res)
    ipps={}
    company_info=[]
    for r in res:
        r=r.strip()
        # print(r)
        c_info=re.split("-",r)
        # print(c_info)
        ipps[c_info[0]]=1
        company_info.append(c_info)

    # print(ipps)
    # print(company_info)

    info={}
    for ipp in ipps:
        for c_i in company_info:
            if ipp in c_i:
              info.setdefault(ipp,[]).append(c_i[1:])

    # print(info)
    return info



# get_info()
