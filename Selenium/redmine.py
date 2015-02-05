#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from selenium import webdriver
from time import sleep
import datetime
import smtplib  
import email.mime.multipart  
from email.mime.text import MIMEText 

class Redmine():    #工时提醒
    def __init__(self):      
        driver = webdriver.Firefox()   
        driver.get("http://redmine.xxx.com/login")
        driver.maximize_window()
        
        sleep(3)
        driver.find_element_by_id("username").send_keys("xxx")
        driver.find_element_by_id("password").send_keys("xxx")
        driver.find_element_by_name("login").click()
        sleep(3)
        driver.get("http://redmine.xxx.com/time_entries?utf8=%E2%9C%93&f%5B%5D=spent_on&op%5Bspent_on%5D=ld&f%5B%5D=&c%5B%5D=project&c%5B%5D=spent_on&c%5B%5D=user&c%5B%5D=activity&c%5B%5D=issue&c%5B%5D=comments&c%5B%5D=hours")
        sleep(2)
        if driver.title == u'耗时 - 详情 - 汇通天下事项跟踪':
            print u'redmine登陆成功！\n'
            num = driver.find_elements_by_xpath("//td[4]/a")        #得到耗时列表的行数
            if len(num) == 30:        #如果等于30，则每页显示50
                driver.find_element_by_link_text('50').click()
            sleep(2)
            nums = driver.find_elements_by_xpath("//td[4]/a")        #再次得到耗时列表的行数
            if len(nums) == 50:
                driver.find_element_by_link_text('100').click()
            sleep(3)
            users = driver.find_elements_by_xpath("//td[4]/a")      #得到每一行的对象
            li = []
            self.temp = str(datetime.date.today()-(datetime.timedelta(days=1)))
            for u in users:         #遍历得到每一行的用户名
                li.append(u.text)
            if u'孙 明昌' in li:       
                print u'孙 明昌'+self.temp+u'日的工时已登记！'
            else:
                print u'孙明昌工时未登记！\n'
                self.sendMail()
        else:
            print u'登陆失败，请重新登陆！\n'
            self.sendMail()
        driver.quit()
        
    def sendMail(self):
        msg = email.mime.multipart.MIMEMultipart()  
        msg['from'] = 'xxx@sina.com'  
        msg['to'] = 'xx@xxx.com' 
        msg['subject'] = u'警告！警告！工时未登记！' 

        text = MIMEText("hello,\n            redmine登陆失败  or  您昨天的工时好像没有登记！",'plain','gbk')  
        msg.attach(text)   
           
        smtp = smtplib.SMTP()  
        smtp.connect('smtp.sina.com','25')  
        smtp.login('xxx@sina.com','password')          
        try:               
            smtp.sendmail('xxx@sina.com','xx@xxx.com',msg.as_string())                     
            smtp.quit()
            print ("发送提醒邮件成功！")  
        except Exception as e:
            print (str(e))
                                         
if __name__ == '__main__':
    red = Redmine()