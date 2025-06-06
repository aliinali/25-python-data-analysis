# -*- coding: utf-8 -*-
"""
Created on Sun Jun  2 15:45:47 2024

@author: Huawei
"""

import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt
import numpy as np
import sys
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from PyQt5.QtWidgets import QDialog,QApplication,QLabel, QLineEdit,QMainWindow,QWidget, QVBoxLayout, QPushButton, QFileDialog, QTableWidget, QTextEdit,QMessageBox
from pylab import mpl

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False
my_style = mpf.make_mpf_style(base_mpf_style='charles', mavcolors = ['red','green','blue'],rc={'font.family': 'SimHei', 'axes.unicode_minus': 'False'})

class Analyzer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('股票数据分析器')
        self.setGeometry(800, 600, 800,600)

        #选择按钮
        self.loadButton = QPushButton('选择Excel文件', self)
        self.loadButton.clicked.connect(self.loadExcelFile)
        layout = QVBoxLayout()
        layout.addWidget(self.loadButton)
        self.setLayout(layout)

     # 打开文件选择对话框
    def loadExcelFile(self):
        filename, _ = QFileDialog.getOpenFileName(self, "选择Excel文件", "", "Excel Files (*.xlsx *.xls);;All Files (*)")
        if filename:
            self.loadExcelData(filename)
            
    #读取表格
    def loadExcelData(self, filename):
        df = pd.read_excel(filename)
        self.search_window = SearchScreen(self,df)
        self.hide()
        self.search_window.show()

class SearchScreen(QMainWindow):
    def __init__(self, parent, df):#为什么变量要按顺序
        super().__init__(parent)
        self.setWindowTitle("股票查询")
        self.setGeometry(800, 600, 800, 600)
        self.df = df
        # 搜索框
        self.code_input = QLineEdit(self)
        self.code_input.setPlaceholderText("输入代码")
        # 搜索按钮
        self.search_btn = QPushButton("搜索", self)
        self.search_btn.clicked.connect(self.on_search_clicked)
        # 返回按钮
        self.back_btn = QPushButton("返回", self)
        self.back_btn.clicked.connect(self.on_back_clicked)
        #推荐按钮
        self.rec_btn = QPushButton('推荐股票',self)
        self.rec_btn.setGeometry(10,10,120,60)
        self.rec_btn.clicked.connect(self.on_rec_clicked)

        layout = QVBoxLayout()
        layout.addWidget(self.code_input)
        layout.addWidget(self.search_btn)
        layout.addWidget(self.back_btn)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
    #搜索按钮link
    def on_search_clicked(self):
        code = self.code_input.text()
        if self.validate_input(code):
            self.details_window = show_details(self, code, self.df)  
            self.details_window.show()
        else:
            self.show_input_error()
    #检查输入
    def validate_input(self, code):
        try:
            int_code = int(code)  
            return int_code in range(self.df['股票代码'].iloc[0],self.df['股票代码'].iloc[self.df.index[-1]])
        except ValueError:
            return False
    #推荐link
    def on_rec_clicked(self):
        dic = {}    
        for i in range(self.df['股票代码'].iloc[0],self.df['股票代码'].iloc[self.df.index[-1]]+1):
            check_df = self.df[self.df['股票代码'] == i]
            dic[i] = sum(check_df['涨跌幅'])
        text = ''
        dic_order=sorted(dic.items(),key=lambda x:x[1],reverse=True)
        for item in dic_order:
            if item[1] >= 0:
                text = text+f'{item[0]} ' 
        

    def show_input_error(self):
        QMessageBox.critical(self, "输入错误", "输入无效，请重新输入。")       
        
    def on_back_clicked(self):
         self.parent().show()
         self.hide()
          

#详细信息页面
class show_details(QMainWindow):
    def __init__(self, parent, code,df):
        super().__init__(parent)
        self.code = code
        self.df = df
        self.dfi = self.individual()
        self.setWindowTitle("详细信息")
        self.setGeometry(800, 600, 1000, 500)
        #返回按钮
        self.back_btn = QPushButton("返回", self)
        self.back_btn.setGeometry(600,400,150,75)
        self.back_btn.clicked.connect(self.on_back_clicked)  
        #折线图按钮
        self.price_btn = QPushButton('价格折线图',self)
        self.price_btn.setGeometry(100,100,150,75)
        self.price_btn.clicked.connect(self.show_price)
        #k线图按钮
        self.k_btn = QPushButton('k线图',self)
        self.k_btn.setGeometry(300,100,150,75)
        self.k_btn.clicked.connect(self.show_k)
        #移动平均线按钮
        self.mav_btn = QPushButton('移动平均线',self)
        self.mav_btn.setGeometry(500,100,150,75)
        self.mav_btn.clicked.connect(self.show_mav)
        #涨跌幅散点图
        self.scat_btn = QPushButton('涨跌幅散点图',self)
        self.scat_btn.setGeometry(100,200,150,75)
        self.scat_btn.clicked.connect(self.show_scat)
        #振幅折线图
        self.amp_btn = QPushButton('振幅折线图',self)
        self.amp_btn.setGeometry(300,200,150,75)
        self.amp_btn.clicked.connect(self.show_amp)
        #换手率柱状图
        self.turn_btn = QPushButton('换手率柱状图',self)
        self.turn_btn.setGeometry(500,200,150,75)
        self.turn_btn.clicked.connect(self.show_turn)
        
     #提取、修改子表   
    def individual(self):
            dfi = self.df[self.df['股票代码'] == int(self.code)]
            dfi.set_index(['日期'],inplace = True)
            dfi.index.name = 'Date'        
            dfi.columns = ['Number','Open','Close','High','Low','Volume','Limit','Amplitude','Turnover']
            return dfi
      #返回键link
    def on_back_clicked(self):
            self.parent().show()
            self.hide()
      #折线图link
    def show_price(self):
            dialog = priceDialog(self.dfi, self)
            dialog.exec_()
     #k线图link
    def show_k(self):
        dialog = kDialog(self.dfi, self)
        dialog.exec_()
      #移动平均线link
    def show_mav(self):
        dialog = mavDialog(self.dfi, self)
        dialog.exec_()
      #散点图link
    def show_scat(self):
        dialog = sactDialog(self.dfi, self)
        dialog.exec_()
      # 振幅link 
    def show_amp(self):
        dialog = ampDialog(self.dfi, self)
        dialog.exec_()
      # 换手率link
    def show_turn(self):
        dialog = turnDialog(self.dfi, self)
        dialog.exec_()
        
      
#k线图 class
class kDialog(QDialog):
    def __init__(self, dfi, parent=None):
        super().__init__(parent)
        self.dfi = dfi
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('k线图')
        self.setGeometry(300, 300, 2000, 800) 
        #作图
        self.fig, self.ax  = mpf.plot(self.dfi,
                         type = 'candle',   
                         style = my_style,
                         ylabel = '价格',
                         xlabel = '时间',
                         volume = True,
                         ylabel_lower = '交易量',
                         returnfig = True)    
                      
        self.canvas = FigureCanvasQTAgg(self.fig)
        
        layout = QVBoxLayout()
        layout.addWidget(self.canvas) 
 
        self.setLayout(layout)
        
    def closeEvent(self, event):
        self.canvas.close()
        plt.close(self.fig)
        super().closeEvent(event)

#mav class
class mavDialog(QDialog): 
    def __init__(self, dfi, parent=None):
        super().__init__(parent)
        self.dfi = dfi
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle('移动平均线图')
        self.setGeometry(300, 300, 2000, 800) 
        #作图
        self.fig, self.ax = mpf.plot(self.dfi,
             type = 'line',
             mav = (5,10,30),
             ylabel = '价格',
             datetime_format='%Y-%m-%d',
             style = my_style,
             returnfig = True
             )             
        self.ax[0].legend(['价格折线','五日移动平均线','十日移动平均线','三十日移动平均线'])        
        self.canvas = FigureCanvasQTAgg(self.fig)
        
       
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)  
 
        self.setLayout(layout)
        
    def closeEvent(self, event):
        self.canvas.close()
        plt.close(self.fig)
        super().closeEvent(event)
        

#折线图 class
class priceDialog(QDialog):
    def __init__(self, dfi, parent=None):
        super().__init__(parent)
        self.dfi = dfi
        self.initUI()
 
    def initUI(self):
        self.setWindowTitle('价格折线图')
        self.setGeometry(300, 300,2000,800) 
            # 创建一个matplotlib图表
        self.fig, self.ax = plt.subplots()  
        self.ax.plot(self.dfi,color = 'blue',linewidth = 0.5) 
        self.ax.set_xlabel('时间')
        self.ax.set_ylabel('价格')
        self.canvas = FigureCanvasQTAgg(self.fig)
 
     
        layout = QVBoxLayout()
        layout.addWidget(self.canvas) 
 
        self.setLayout(layout) 
        
    def closeEvent(self, event):
        self.canvas.close()
        plt.close(self.fig)
        super().closeEvent(event)

#散点图 class      
class sactDialog(QDialog):
    def __init__(self, dfi, parent=None):
        super().__init__(parent)
        self.dfi = dfi
        self.initUI()
     
    def initUI(self):
        self.setWindowTitle('涨跌幅散点图')
        self.setGeometry(300, 300,2000,800) 
        my_color = ['#228B22' if i > 0 else '#A52A2A' for i in self.dfi['Limit'].values]
        #画图
        self.fig,self.ax = plt.subplots()
        self.ax.scatter(self.dfi.index,self.dfi['Limit'],color = my_color)
        self.ax.set_xlabel('时间')
        self.canvas = FigureCanvasQTAgg(self.fig)
        
        layout = QVBoxLayout() 
        layout.addWidget(self.canvas)
        
        self.setLayout(layout)
        
    def closeEvent(self, event):
        self.canvas.close()
        plt.close(self.fig)
        super().closeEvent(event)

        
#振幅折线图 class
class ampDialog(QDialog):
    def __init__(self, dfi, parent=None):
        super().__init__(parent)
        self.dfi = dfi
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('振幅折线图')
        self.setGeometry(300, 300,2000,800) 
        #画图
        self.fig,self.ax = plt.subplots()
        self.ax.plot(self.dfi.index,self.dfi['Amplitude'],color = 'green',linewidth = 0.5)
        self.ax.set_xlabel('时间')
        self.canvas = FigureCanvasQTAgg(self.fig)
        
        layout = QVBoxLayout() 
        layout.addWidget(self.canvas)
        
        self.setLayout(layout)
        
    def closeEvent(self, event):
        self.canvas.close()
        plt.close(self.fig)
        super().closeEvent(event)

#换手率柱状图class
class turnDialog(QDialog):
    def __init__(self, dfi, parent=None):
        super().__init__(parent)
        self.dfi = dfi
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('换手率柱状图')
        self.setGeometry(300, 300,2000,800) 
        #画图
        self.fig,self.ax = plt.subplots()
        self.ax.bar(self.dfi.index,self.dfi['Turnover'],color = 'red',width = 0.3)
        self.ax.set_xlabel('时间')
        self.ax.set_ylabel('换手率')
        self.canvas = FigureCanvasQTAgg(self.fig)
        
        layout = QVBoxLayout() 
        layout.addWidget(self.canvas)
        
        self.setLayout(layout)
        
    def closeEvent(self, event):
        self.canvas.close()
        plt.close(self.fig)
        super().closeEvent(event)
   
 
# 创建实例
app = QApplication(sys.argv)
start_window = Analyzer()
start_window.show()
sys.exit(app.exec())
        
        
        
        
        

