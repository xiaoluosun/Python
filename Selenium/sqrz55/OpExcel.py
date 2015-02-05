#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import xlrd
from xlrd import open_workbook
from xlutils.copy import copy
from ConnMysql import ConnMysql

class OpExcel(object):
    def __init__(self):        
        file = xlrd.open_workbook("E:\WorkSpace\python34Demo\data\\运单导入模板.xlsx")  
        sheet = file.sheet_by_index(0)
        self.sheets = copy(file)
        self.table = self.sheets.get_sheet(0)
        
        self.conn = ConnMysql()
        self.conn.selectSql()
               
    def rExcel(self):
        print "生成运单模板中，请稍等。。。"        
        row = 1
        col = 0
        for each in self.conn.results:
            if row == 10:
                pass
            else:
                self.conn.getTime()
                self.table.write(row, col, each)                      
                self.table.write(row, col+1, self.conn.temp+row)
                self.sheets.save("E:\WorkSpace\python34Demo\data\\运单导入模板.xlsx")
                row += 1
        self.conn.closeSql()