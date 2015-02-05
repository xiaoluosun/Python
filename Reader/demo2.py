#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')

import pymysql

class ConnPySql(object):
    def __init__(self):
        self.conn = pymysql.connect(host='localhost',user='sun',passwd='111111',db='python',charset='utf8') 
        self.cur = self.conn.cursor() 
        
    def selectSql(self):
        self.cur.execute("show tables;")
        tablename = self.cur.fetchall()
    
        if len(tablename) > 0:        #判断数据表是否存在
            selectSql = ("SELECT * FROM py_books")      #查询数据库数据
            self.cur.execute(selectSql)      
            self.results = self.cur.fetchall()       
        else:
            self.cur.execute("CREATE TABLE py_books\
                            (ID int NOT NULL AUTO_INCREMENT,\
                            PRIMARY KEY(ID),\
                            filename varchar(100),\
                            filewriter varchar(100),\
                            filefix varchar(100),\
                            filesize varchar(100),\
                            filectime varchar(100),\
                            fileatime varchar(100),\
                            filestatus varchar(100),\
                            filepath varchar(100)\
                            )")
            
            self.cur.execute("SELECT * FROM py_books")      #查询数据库数据    
            self.results = self.cur.fetchall()  
            
    def selectRow(self):       #统计py_books表的行数
        self.cur.execute("select count(*) from py_books")      
        self.row = self.cur.fetchall() 
          
    def selectSta(self,filename):
        self.cur.execute(str('select filestatus from py_books where filename = "' + filename + '"'))     
        self.resta = self.cur.fetchall()
            
    def pathSql(self,filename):
        pathsql = (u"SELECT filepath FROM py_books WHERE filename = '"+filename+"'")       
        self.cur.execute(str(pathsql))      
        self.repath = self.cur.fetchall()    
             
    def insertSql(self,rebooks):        
        insertsql = ('INSERT INTO py_books VALUES(Null,"'+rebooks[0]+'","'+rebooks[1]+'","'+rebooks[2]+'","'+rebooks[3]\
                         +'","'+rebooks[4]+'","'+rebooks[5]+'","'+rebooks[6]+'","'+rebooks[7]+'")')
        
        self.cur.execute(str(insertsql))
        self.conn.commit()
    def updateSta(self,filename):
        self.cur.execute(str('UPDATE py_books SET filestatus = 1 where filename = "'+ filename + '"')) 
        self.conn.commit()
        
    def closeSql(self):
        self.cur.close()
        self.conn.close()
        