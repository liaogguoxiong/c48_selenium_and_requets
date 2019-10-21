#!/usr/bin/env python 
# -*- coding: utf-8 -*-
# @Time             : 2019-10-19 15:01
# @Author           : lgx
# @project_name     : c48_selenium_and_requets
# @File             : main_process.py
# @Des: 主程序

from dzfp_c48 import *
from deal_input_data import *
from jsp_service_status import *


def main():
    info=deal_method()

    for company_info in info:
        ipp=company_info
        cs = c48_sys(ipp)
        for j in info[company_info]:
            shuihao=j[0]
            cs.login_c48()
            cookies_info = cs.get_cookie()
            cookies = {}
            for c in cookies_info:
                cookies[c['name']] = c['value']
            status=get_status(cookies,shuihao)
            print("{}的状态是:{}".format(shuihao,status))
        cs.close_browse()

if __name__ == '__main__':
    main()
