#!/usr/bin/env python
#-*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import os,chardet
import time
from demo2 import ConnPySql
from PyQt4 import QtCore, QtGui

class MyWindow(QtGui.QMainWindow,QtGui.QDialog):
    def __init__(self):
        QtGui.QMainWindow.__init__(self) 

        self.setWindowTitle(u"流弊轰轰阅读器")
#        self.showMaximized()    #窗口最大化, 调试过程中不知道为啥不管用了？！
        screen = QtGui.QDesktopWidget().screenGeometry()    #窗口最大化
        self.resize(screen.width(),screen.height())
                    
        self.conn = ConnPySql()     #调用连接数据库类
        
        toolbar = self.addToolBar(u'工具栏')    #工具栏对象
        
        refresh = QtGui.QAction(QtGui.QIcon('icons/refresh.jpg'),u'刷新',self) 
        refresh.setShortcut('Ctrl+F5')
        refresh.setStatusTip(u'刷新页面')
        self.connect(refresh,QtCore.SIGNAL('triggered()'),self.onRefresh)                      
        toolbar.addAction(refresh)
        
        menubar = self.menuBar()    #菜单栏对象
        menubar.setFont(QtGui.QFont("Times", 10, QtGui.QFont.Bold))     #设置菜单栏字体
        
        self.file = menubar.addMenu(u'&文件(F)')
        openf = self.file.addAction(u'导入')
        self.connect(openf, QtCore.SIGNAL('triggered()'),self.onOpen)
        
        close = self.file.addAction(u'退出')
        self.connect(close, QtCore.SIGNAL('triggered()'),self.onClose)
        
        self.file = menubar.addMenu(u'&工具(T)')
        lebel = self.file.addAction(u'添加书签')
        self.connect(lebel, QtCore.SIGNAL('triggered()'),self.onLabel)
        
        option = self.file.addAction(u'选项')
        self.connect(option, QtCore.SIGNAL('triggered()'),self.onOption)
        
        self.file = menubar.addMenu(u'&帮助(H)')
        about = self.file.addAction(u'关于')
        self.connect(about, QtCore.SIGNAL('triggered()'),self.onAbout)  
              
    def onRefresh(self):
        self.showInfo()
        
    path = ''    
    def onOpen(self):   #文件导入
        self.path = QtGui.QFileDialog.getOpenFileName(self, u'选择文件')
        if self.path != '':
            if self.path.split('.', 1)[1] != 'txt':     #只能添加.txt格式文件
                QtGui.QMessageBox.warning(self, u'提示',u'只能导入txt文件')
            else:
                self.fileInfo()
        
    def onClose(self):  #关闭窗体
        self.close()
        
    def onLabel(self):      #添加书签
        QtGui.QMessageBox.warning(self, u'提示',u'暂不可用！')   
                
    def onOption(self):     #选项
        QtGui.QMessageBox.warning(self, u'提示',u'暂不可用！')
        
    def onAbout(self):     #帮助
        QtGui.QMessageBox.warning(self, u'提示',u'暂不可用！')
        
    temp = []        
    def outSelect(self,Item=None):      #在列表点击文件后，转码文件并进去内容页面。
        if Item == None:
            return        
        self.conn.pathSql(Item.text())
        try:
            self.conn.selectSta(Item.text())
            
            if self.conn.resta[0][0] == '0':        #判断文件状态，如果为0则先转码再打开，如果为1直接打开。
                op = open(self.conn.repath[0][0],'r')   
                content = []
                while True:         #转换文件编码
                    line = op.readline()
                    try:
                        content.append(line.decode("GB2312").encode("UTF-8"))
                    finally:
                        print op.next()
                            
                    if len(line) == 0:
                        break
                op.close()
                ops = open(self.conn.repath[0][0],'w')
                ops.writelines(content)
                ops.close()  
                
                fopen = open(self.conn.repath[0][0],'rb')       
            else:
                fopen = open(self.conn.repath[0][0],'rb')
                
        except IOError:
            print ("文件打开失败")       
        else:           
            for line in fopen.readlines()[0:100]:
                self.temp.append(line)
            temp = ''.join(self.temp)
            text = QtGui.QTextBrowser()
            text.append(unicode(temp, 'utf8', 'ignore'))
            self.setCentralWidget(text)
            
            self.conn.updateSta(Item.text())
            fopen.close()          
      
    def fileInfo(self):       #通过打开文件的路径，取得文件的属性
#        name = os.path.basename(self.path)   #去掉路径，只保留文件名和后缀
        name = self.path.split("/")[-1]       #去掉路径，只保留文件名和后缀
        size = ('%.2F'%(os.path.getsize(self.path) / 1024 / 1024))+'M'    #获得文件大小，单位为M
        timeStamp = os.path.getctime(self.path)    #获得文件创建时间的时间戳，并转换为日期格式。
        timeArray = time.localtime(timeStamp)
        otherStyleTime = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)       
        timeStamps = os.path.getatime(self.path)    #获得文件访问时间的时间戳，并转换为日期格式。
        timeArrays = time.localtime(timeStamps)
        otherStyleTimes = time.strftime("%Y-%m-%d %H:%M:%S", timeArrays)
        
        filewriter = u'佚名'
        filestatus = '0'

        rebooks = [name.split('.', 1)[0],filewriter,name.split('.', 1)[1],\
                   size,otherStyleTime,otherStyleTimes,filestatus,self.path]
             
        self.conn.insertSql(rebooks)        #把文件的属性传给数据库类，并保存到数据库  

#        self.conn.closeSql()        #调用关闭数据库方法    如开启，则每次只能导入一个文件。
    
    
    def showInfo(self):     #从数据库查询的结果列表展示到Table
        self.count = 0
        self.conn.selectSql()       #查询数据并返回结果
        self.conn.selectRow()      
        self.table = QtGui.QTableWidget(self.conn.row[0][0],8)      #根据数据库py_books表的行数创建Table       
        self.table.setHorizontalHeaderLabels([u'名称',u'作者',u'类型',u'大小',
                                              u'添加时间',u'阅读时间',u'状态',u'路径'])              
        self.setCentralWidget(self.table)       #把Table应用到QMinWindow
        
        self.table.itemClicked.connect(self.outSelect)      #打印文件内容
                                       
        for eachstr in self.conn.results:                          
            self.filename = QtGui.QTableWidgetItem(eachstr[1])
            self.filewriter = QtGui.QTableWidgetItem(eachstr[2])    
            self.filefix = QtGui.QTableWidgetItem(eachstr[3])
            self.filesize = QtGui.QTableWidgetItem(eachstr[4])
            self.filectime = QtGui.QTableWidgetItem(str(eachstr[5]))
            self.fileatime = QtGui.QTableWidgetItem(str(eachstr[6]))
#            self.filestatus = QtGui.QTableWidgetItem(eachstr[7])
            if eachstr[7] == '0':
                self.filestatus = QtGui.QTableWidgetItem(u'未阅读')
            elif eachstr[7] == '1':
                self.filestatus = QtGui.QTableWidgetItem(u'已阅读')
                
            self.filepath = QtGui.QTableWidgetItem(eachstr[8])
            
            self.table.setItem(self.count,0,self.filename)
            self.table.setItem(self.count,1,self.filewriter)
            self.table.setItem(self.count,2,self.filefix)       
            self.table.setItem(self.count,3,self.filesize)
            self.table.setItem(self.count,4,self.filectime)
            self.table.setItem(self.count,5,self.fileatime)
            self.table.setItem(self.count,6,self.filestatus)  
            self.table.setItem(self.count,7,self.filepath)
            
            self.count += 1

        for x in range(self.table.columnCount()):    #设置表头属性
            headFont = QtGui.QFont("song", 12, QtGui.QFont.Bold)
            headItem = self.table.horizontalHeaderItem(x)   #获得水平方向表头的Item对象  
            headItem.setFont(headFont)                        #设置字体
        textFont = QtGui.QFont("song", 10)      #设置列表字体
        self.table.setFont(QtGui.QFont(textFont))
        
        self.table.setColumnWidth(0,200)        #设置列宽
        self.table.setColumnWidth(4,200)
        self.table.setColumnWidth(5,200)    
        self.table.setColumnWidth(7,365)

        self.table.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)      #table不可修改
        self.table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)     #点击选中整行
        self.table.verticalHeader().setVisible(False)       #侧表头不可见
        self.table.setShowGrid (False)      #隐藏网格
        self.table.setAlternatingRowColors(True)        #隔行换颜色
        self.table.setStyleSheet("selection-background-color:lightblue;")       #设置选中背景色
        self.table.setFocusPolicy(False)        #隐藏选中虚线
        
if __name__ == '__main__':                              
    app = QtGui.QApplication(sys.argv)   
    mywindow = MyWindow()
    mywindow.show()
    mywindow.showInfo()
    app.exec_()