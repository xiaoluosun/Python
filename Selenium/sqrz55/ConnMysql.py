#encoding=utf-8

import pymysql
import time

class ConnMysql(object):
    def __init__(self):
        self.conn = pymysql.connect(host='192.168.x.x',user='tester',passwd='tester890__',db='ips_sqrz',charset='utf8') 
        self.cur = self.conn.cursor()
        
    def selectSql(self):
        selectSql = ("SELECT secondprojectno FROM ips_smallproject_info")      #��ѯ��ݿ����
        self.cur.execute(selectSql)      
        self.results = self.cur.fetchall() 
    
    def getTime(self):
        self.temp = int(time.strftime('%Y%m%d%H%M%S',time.localtime(time.time())))
        
    def closeSql(self):    
        self.cur.close()
        self.conn.close() 