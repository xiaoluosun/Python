#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

from selenium import webdriver
import time,sys
from OpExcel import OpExcel

class ImportOrder(object):
    def __init__(self):
        driver = webdriver.Firefox()   
        driver.get("http://sqrz55.ips.cn")
        driver.maximize_window()  
         
        time.sleep(1.5)
        driver.find_element_by_id("username").send_keys("xxx")
        driver.find_element_by_id("password").send_keys("xx")
        driver.find_element_by_class_name("login_btn").click()
        
        time.sleep(2)       
        if driver.title == u'首页 - G7':
            print '登陆成功'            
            driver.get("http://sqrz55.ips.cn/ordercenter/import.html")
            
            time.sleep(1)       #直接为导入控件赋文件的绝对路径
            driver.find_element_by_xpath('//*[@id="importfile"]').\
            send_keys(u"E:\WorkSpace\python34Demo\data\\运单导入模板.xlsx")            
            driver.find_element_by_id("btnsubmit").click()           
            time.sleep(2)
            driver.find_element_by_class_name("ui_state_highlight").click()
            
            succeed = driver.find_element_by_xpath("//span[@id='success_count']").text      #得到成功导入和失败导入的数目
            error = driver.find_element_by_xpath("//span[@id='error_count']").text                  
            if succeed >= 0:
                print '成功导入'+succeed+'条数据'
                print '失败'+error+'条数据'       
        else:
            print '登陆失败，请重新登陆'
        
        driver.quit()
                   
if __name__ == '__main__':
    ex = OpExcel()
    ex.rExcel()
    io = ImportOrder()