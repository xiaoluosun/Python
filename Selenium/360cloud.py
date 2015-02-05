#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
  
from selenium import webdriver
from time import sleep
class CloudLogin():
    def __init__(self):      
        driver = webdriver.Firefox()   
        driver.get("http://yunpan.360.cn")
        driver.maximize_window()
        
        sleep(2)
        driver.find_element_by_id("loginAccount").send_keys("xxx")
        driver.find_element_by_id("lpassword").send_keys("xxx")
        driver.find_element_by_id("loginSubmit").click()
        
        sleep(3)
        if driver.title == u'360云盘 - 我的云盘':
            print '登陆成功!\n'           
            driver.get("http://c17.yunpan.360.cn/my?p=signin")        
        else:
            print '登陆失败，请重新登陆！\n'
            
        driver.quit()
if __name__ == '__main__':
    cl = CloudLogin()