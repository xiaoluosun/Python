#!/usr/bin/env python
#-*- coding:utf8 -*-

import sys
reload(sys)
sys.setdefaultencoding('gbk')
import urllib,urllib2
import re,os
import threading
from bs4 import BeautifulSoup
from time import sleep

class GetHtml():
    def __init__(self):  
        headers = { #伪装为浏览器抓取    
                   'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'    
        }
        html = "http://tieba.baidu.com/f?kw=摄影"   #摄影贴吧的首页链接
        self.req = urllib2.Request(html)
        self.req.add_header('User-Agent',headers)  
        
        content = urllib2.urlopen(self.req).read()
        soup = BeautifulSoup(content)
        aLinks = soup.find_all('a')     #定位a标签
        self.urls = []
        for aLink in aLinks :
            href = str(aLink.get('href'))       #a标签内href的属性
            link = re.compile("/p/\d{10}")      #正则筛选出符合条件的数据,比如 /p/1234567890
            if link.findall(href):
                url = link.findall(href)        
                self.urls += url                #结果合并成一个list
                
    def getImg(self):
        for i in self.urls:         #循环进入每个帖子内，查找jpg后缀的文件，并download
            try:
                self.page = urllib2.urlopen('http://tieba.baidu.com'+i,timeout=20).read()
            except urllib2.URLError, e:
                print u'打开失败，',e
            reg = r'src="(.+?\.jpg)" pic_ext'       
            imgre = re.compile(reg)
            imglist = re.findall(imgre,self.page) 
            
            m = re.search("<title>.*</title>", self.page)        #匹配<title>
            t = m.group().strip("</title>").strip(u"_摄影吧_百度贴吧")         #去除<title>和后缀"_摄影吧_百度贴吧"
            ts = t.strip(u": / \\ ? * \" < > |")        #去除title中文件夹不允许命名的字符，但是/一直去不掉？啥原因。。。
            title = "".join(ts.split())         #去除空格
            self.titles = "".join(title.split('/'))      #再去除一次/符号
            
            if os.path.exists(u"E:\\WorkSpace\\picture\\"+self.titles) == False:     #判断文件夹是否存在，没有则创建
                os.mkdir(u"E:\\WorkSpace\\picture\\"+self.titles)                        
                       
            threads = []
            self.s = 0
            for im in imglist:      #多线程调用下载函数           
                t = threading.Thread(target=self.downImg, args=(im,))
                threads.append(t)
                
                threads[self.s].start()
                threads[self.s].join()
                self.s += 1
            
            if self.s > 0:       #输出有图片的帖子title和图片数量   
                m = re.search("<title>.*</title>", self.page)
                print m.group().strip("</title>").strip(u"_摄影吧_百度贴吧")+u',下载完成！'     # 这里输出结果                
                print self.s    
                          
    def downImg(self,im):      #下载到自定义目录      
        sleep(5)        
        try:
            urllib.urlretrieve(im,"E:\\WorkSpace\\picture\\"+self.titles+"\\%s.jpg" % self.s,reporthook=self.reporthook)
        except IOError,e:
            print "%s.jpg" % self.s+u'下载失败,',e
            
    def reporthook(self,blocknum,blocksize,totalsize):
        '''回调函数
            @blocknum: 已经下载的数据块
            @blocksize: 数据块的大小
            @totalsize: 远程文件的大小
        '''       
        percent = 100 * blocknum * blocksize / totalsize
        if percent > 100:
            percent = 100
        print "%s.jpg" % self.s+u'已下载'+'%d%%' % percent

if __name__ == "__main__":
    gh = GetHtml()
    gh.getImg()