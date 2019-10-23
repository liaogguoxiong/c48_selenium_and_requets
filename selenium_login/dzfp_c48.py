'''
@author: lgx
@Email:297979949@qq.com
@project: export_data
@file: dzfp_c48.py
@time: 2019-10-10 9:31
@desc:实现电子发票管理平台的各项功能
'''

from selenium import webdriver

import time,datetime
import selenium.common.exceptions
from recognize_verify_code import *
from selenium.webdriver.support.select import Select
from logging_class import *

class c48_sys():

    def __init__(self,ipp,uname="admin",passwd="Aisino123+"):
        """
        :param ipp:ip加端口号
        """
        self.ipp = ipp
        self.login_url = 'http://{}/zzs_kpfw_manager/login.htm'.format(ipp)  # c48登录的url
        self.base_url = 'http://{}/zzs_kpfw_manager'.format(ipp)  # 跳转到其他功能的基础url

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('headless')
        self.driver = webdriver.Chrome(chrome_options=chrome_options)   # 实例化selenium.webdriver
        """
        ipp为192.168.20.197:8081的时候
        账号密码不是默认的
        """
        if self.ipp == "192.168.20.197:8081":
            self.uname=uname
            self.passwd="Admin123_"
        else:
            self.uname = uname
            self.passwd = passwd





    def login_c48(self):
        """
        实现登录c48的功能,识别验证码
        :return: 0 表示登录成功
        """
        login_screen_path = "C:/2/screen.png"   # 存c48登录界面的截图位置
        verify_code_path="C:/2/verfy_code.png"  # 保存验证码的图片的位置

        self.driver.get(self.login_url) #打开url
        m="登录的url为:{}".format(self.login_url)
        rz.log(m)
        self.driver.implicitly_wait(8)  # 隐形等待8秒,等待浏览器加载完
        self.driver.maximize_window()   # 浏览器窗口最大化


        """
        死循环,不停滴识别验证码
        直到识别登录成功,才返回
        """
        while True:

            self.driver.save_screenshot(login_screen_path)  # 截取整个浏览器的图片,并保存起来
            location = self.driver.find_element_by_id("gencode").location   # 取验证码的位置信息
            size = self.driver.find_element_by_id("gencode").size   # 获取验证码的大小


            """
            根据验证码的大小和在整个登录界面
            截图的位置来裁剪出验证码
            
            注意:#坑爹,电脑分辨率为100%的时候才能够正确截取,其他大小的时候无法正确截取
            
            
            """
            coordinate = (int(location['x']), int(location['y']), int(location['x'] + size['width']),
                          int(location['y'] + size['height']))

            im = Image.open(login_screen_path)

            im_1 = im.crop(coordinate)  # 裁剪验证码

            im_1.save(verify_code_path) # 保存截取成功的验证码


            """
            传入保存验证码图片的位置,
            调用recognize_code()进行验证码识别
            返回识别的验证码,code为字符串类型
            """
            code=recognize_code(verify_code_path)
            m1="识别出的验证码:{}".format(code)
            rz.log(m1)
            """
            由于识别的效率太低,code经常为
            None,当为None时就是识别不到,
            重新刷新网页,再次获取验证码
            """
            if code == None:
                time.sleep(1)
                m2="识别为None,重新刷新网页继续识别"
                rz.log(m2)
                self.driver.refresh()
                continue

            elif len(code) != 4:
                time.sleep(1)
                m9 = "验证码不足4位,重新刷新网页继续识别"
                rz.log(m9)
                self.driver.refresh()
                continue


            """
            识别到验证码之后,
            输入账号密码验证码
            提交登录
            """
            self.driver.find_element_by_id("user_account").send_keys(self.uname)   # 输入账号
            m3="输入账号....."
            rz.log(m3)
            time.sleep(1)
            self.driver.find_element_by_id("password").send_keys(self.passwd)  # 输入密码
            m4="输入密码....."
            rz.log(m4)
            time.sleep(1)
            self.driver.find_element_by_id("validCode").send_keys(code) # 输入验证码
            m5="输入验证码......"
            rz.log(m5)
            time.sleep(1)
            self.driver.find_element_by_class_name("button_login").click()  # 点击登录按钮
            m6="登录...."
            rz.log(m6)
            time.sleep(3)

            """
            由于验证码不一定识别成功,
            我们就得需要判断此时在不在登录成功之后的页面
            登录成功之后的页面的源代码有[欢迎您，系统管理员]
            我们可以根据此来做判断
            如果成功的话,返回0
            失败的话,重新请求登录页面的url
            
            注意:本来是想登录失败之后,重新刷新网页记性了,但是
            验证码的框会显示出东西挡住了截图
            """
            word="欢迎您，系统管理员"

            if word in self.driver.page_source:
                m7="登录成功"
                rz.log(m7)
                time.sleep(3)
                return 0

            else:
                m8="验证码不正确,重新请求网页"
                rz.log(m8)
                time.sleep(2)
                self.driver.get(self.login_url)



    def huizong_fp(self,shuihao,fj_num):
        """
        实现月度统计的功能
        :param shuihao:公司的税号
        :param fj_num:金税盘的分机号
        :return:
        """

        url="/tax/monthly_statistics/list.htm"   # c48的功能url都是通过基本的url加上专属的url组合而成
        huizong_url=self.base_url+url
        year = datetime.datetime.now().year     # 年份
        mon = datetime.datetime.now().month    # 月份
        """
        由于月度汇总都是汇总上个月的,
        1月份导的是12月份的
        """
        if mon == 1:
            mon = 12

        self.driver.get(huizong_url)
        m="打开[月度统计]的界面"
        rz.log(m)
        self.driver.implicitly_wait(8)
        time.sleep(1)
        """
        传入税号,公司名称会根据税号带出
        """
        self.driver.find_element_by_xpath("//input[@id='_easyui_textbox_input4']").send_keys(shuihao)
        m1="输入税号:{}".format(shuihao)
        rz.log(m1)
        time.sleep(1)
        self.driver.find_element_by_xpath("//input[@id='_easyui_textbox_input6']").send_keys(fj_num)    # 传入分机号
        m2="输入分机号:{}".format(fj_num)
        rz.log(m2)
        time.sleep(1)
        self.driver.find_element_by_id("search_year").send_keys(year)   # 传入年份
        m3="输入年份:{}".format(year)
        rz.log(m3)
        time.sleep(1)
        self.driver.find_element_by_id("search_month").send_keys(mon-1) # 传入月份
        m4="输入月份:{}".format(mon-1)
        rz.log(m4)
        time.sleep(1)
        """
        发票种类是个下拉标签select,
        使用Select方法来选择
        """
        Select(self.driver.find_element_by_name("search_fpzl")).select_by_value("51")
        m5="选择发票种类:电子发票"
        rz.log(m5)
        time.sleep(1)
        self.driver.find_element_by_id("queryInfo").click()     # 点击查询按钮
        m6="查询......"
        rz.log(m6)
        time.sleep(2)
        self.driver.find_element_by_id("doExportBntPdf").click()    #点击导出pdf按钮
        m7="导出pdf...."
        rz.log(m7)
        time.sleep(2)
        """
        判断pdf是否下载成功
        使用os.listdit列出下载
        目录下的所有文件
        """
        f_path="C:/Users/lgx/Downloads"     # 保存pdf文件的路径
        f_list=os.listdir(f_path)           # 列出保存pdf路径下的所有文件,是一个列表
        m8="{}导出pdf文件成功".format(shuihao)
        m9="{}导出pdf文件失败".format(shuihao)
        exist=1     # 用作判断是否找到的标志,0为找到,1为没找到

        for name in f_list:
            if shuihao in name:
                rz.log(m8)
                exist=0

        if exist !=0:
            rz.log(m9,30)   # 下载目录下找不到相关税号的pdf文件



    def service_status(self,shuihao,name):
        """
        查看金税盘的服务状态
        需要传入公司的税号,名称
        :param shuihao:公司的税号
        :return:
        """
        m1="打开{}的[服务状态监控]页面....".format(shuihao)
        m2="输入税号{}".format(shuihao)
        m3="点击查询"

        ss_url="/statistic/serviceStatus/list.htm"      #金税盘服务页面的后缀url
        target_url=self.base_url+ss_url
        self.driver.get(target_url)
        rz.log(m1)
        self.driver.maximize_window()
        self.driver.implicitly_wait(8)
        time.sleep(2)
        self.driver.find_element_by_id("_easyui_textbox_input3").send_keys(shuihao)
        rz.log(m2)
        time.sleep(5)
        self.driver.find_element_by_id("query").click()
        rz.log(m3)
        time.sleep(2)
        try:
            status=self.driver.find_element_by_xpath("/html[1]/body[1]/form[jieshun]/div[jieshun]/table[1]/tbody[1]/tr[1]/td[6]/span[1]").text
            m4="获取到{}的服务状态为:{}".format(name,status)
            rz.log(m4)
            rz.log("\n\n\n")
            time.sleep(2)
            return status
        except selenium.common.exceptions.NoSuchElementException:
            mes=self.driver.find_element_by_xpath("//div[@class='text']//span//font").text
            rz.log(mes,30)
            return mes



    def purchase_fp(self,shuihao):
        """
        用于领购发票
        :return:
        """
        p_url="/invoice/purchase/list.htm"      # 购买发票页面的后缀url
        purchase_url=self.base_url+p_url        # 购买发票页面的完整url
        self.driver.get(purchase_url)           # 单独以一个页面打开申领发票页面
        rz.log("打开发票领购页面......")
        self.driver.maximize_window()
        self.driver.implicitly_wait(8)
        time.sleep(2)
        self.driver.find_element_by_id("_easyui_textbox_input4").click()
        self.driver.find_element_by_id("_easyui_textbox_input4").send_keys(shuihao)
        m2="输入税号:{}".format(shuihao)
        rz.log(m2)
        time.sleep(2)
        self.driver.find_element_by_id("queryInfo").click()
        rz.log("点击查询....")
        time.sleep(2)
        self.driver.find_element_by_link_text("局端票源查询").click()
        rz.log("点击局端票源查询......")
        self.driver.implicitly_wait(8)
        time.sleep(2)
        exist_sign="局端没有可以下载票源"
        res=self.driver.find_element_by_xpath("/html[1]/body[1]/div[1]/div[jieshun]/span[1]/font[1]").text
        m1="{}无可下载票源".format(shuihao)
        if exist_sign in res:
            rz.log(m1)
        else:
            fp_num=self.driver.find_element_by_xpath("/html[1]/body[1]/form[1]/div[jieshun]/table[1]/tbody[1]/tr[1]/td[8]").text
            m3="{}可领购发票数量为:{}".format(shuihao,fp_num)
            rz.log(m3)
            self.driver.get(purchase_url)
            self.driver.implicitly_wait(8)
            rz.log("返回发票领购页面....")
            self.driver.find_element_by_id("_easyui_textbox_input4").click()
            self.driver.find_element_by_id("_easyui_textbox_input4").send_keys(shuihao)
            m4="输入要领购发票的税号:{}".format(shuihao)
            rz.log(m4)
            time.sleep(2)
            self.driver.find_element_by_id("queryInfo").click()
            rz.log("点击查询按钮....")
            time.sleep(2)
            self.driver.find_element_by_xpath("/html[1]/body[1]/form[jieshun]/div[jieshun]/table[1]/tbody[1]/tr[1]/td[6]/input[1]").click()
            self.driver.find_element_by_xpath("/html[1]/body[1]/form[jieshun]/div[jieshun]/table[1]/tbody[1]/tr[1]/td[6]/input[1]").send_keys(fp_num)
            m5="输入要领购的发票份数:{}".format(fp_num)
            rz.log(m5)
            time.sleep(2)
            self.driver.find_element_by_link_text("网上领票").click()
            rz.log("点击网上领票....")
            res_mes=self.driver.find_element_by_xpath("/html[1]/body[1]/div[1]/div[jieshun]/span[1]/font[1]").text
            sucess_sign="申请结果【成功】"
            if sucess_sign in res_mes:
                rz.log(res_mes)
            else:
                rz.log(res_mes,30)
                time.sleep(1)
                rz.log("领票结束....")
            rz.log("\n\n\n")




    def upload_fp(self,shuihao):
        """
        用于上传发票
        :return:
        """
        u_url="/statistics/invoiceuploadStatus/list.htm"
        upload_url=self.base_url+u_url
        n=0

        while n < 3:
            self.driver.get(upload_url)
            self.driver.maximize_window()
            self.driver.implicitly_wait(8)

            rz.log("正在打开发票上传页面....")
            time.sleep(2)
            self.driver.find_element_by_id("_easyui_textbox_input4").click()
            self.driver.find_element_by_id("_easyui_textbox_input4").send_keys(shuihao)
            m="输入税号:{}".format(shuihao)
            rz.log(m)
            time.sleep(2)
            self.driver.find_element_by_id("query").click()
            rz.log("条件输入完成,正在查询.....")
            time.sleep(2)

            upload_buttons=self.driver.find_elements_by_link_text("上传")     # 用于判断是否需要上传

            if len(upload_buttons) != 0:
                m1="需要点击的上传按钮个数:{}".format(len(upload_buttons))
                rz.log(m1)
                self.driver.find_element_by_link_text("上传").click()
                rz.log("上传发票中.....")
                self.driver.implicitly_wait(8)
                time.sleep(2)
                """
                有时候网络不好或者
                税局的原因,会导致超时
                如果超时,重复调用3次
                """
                try:
                    res_mes = self.driver.find_element_by_xpath("/html[1]/body[1]/div[jieshun]/div[1]/div[jieshun]/span[1]/font[1]").text
                    rz.log(res_mes)
                    rz.log("检查是否还有未上传的发票.....")
                    time.sleep(2)
                except selenium.common.exceptions.NoSuchElementException:
                    rz.log("504 Gateway Time-out...",40)
                    n+=1
                    mes="网络超时,第{}次调用".format(n+1)
                    rz.log(mes)
                    time.sleep(2)

            else:
                rz.log("无可上传的发票....")
                time.sleep(2)
                break


    def get_cookie(self):
        cookies=self.driver.get_cookies()
        return cookies

    def s_source(self):
        res=self.driver.page_source
        return  res



    def close_browse(self):
        time.sleep(3)
        self.driver.quit()
        m="关闭{}页面".format(self.login_url)
        rz.log(m)
        rz.log("\n\n\n")



"""
初始化日志
"""
log_path = "log.log"     # 日志的保存路径
rz=rizhi()                                     # 实例化日志的对象
rz.send_to_file(log_path)                      # 输出到日志文件中
rz.send_to_stdout()                            # 输出到屏幕














