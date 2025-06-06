# -*- coding: utf-8 -*-
"""
Created on Wed May 29 16:42:08 2024

@author: Huawei
"""


#导入
import pandas as pd
import mplfinance as mpf
import numpy as np
import matplotlib.pyplot as plt
from pylab import mpl
import matplotlib.ticker as ticker

mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False

#数据读入
df = pd.read_excel("金融-精简化股市数据分析.xlsx")
   
#TASK1 
#(一）数据统计部分
#100支股票243天内各数据求和 数据储存在各字典中
#100支股票243天内各数据求平均 数据储存在各字典中

sum_open_price_dic = {}
sum_close_price_dic = {}
sum_highest_price_dic = {}
sum_lowest_price_dic = {}
sum_trade_volume_dic = {}
sum_price_limit_dic = {}
sum_amplitude_dic = {}
sum_turnover_dic = {}

ave_open_price_dic = {}
ave_close_price_dic = {}
ave_highest_price_dic = {}
ave_lowest_price_dic = {}
ave_trade_volume_dic = {}
ave_price_limit_dic = {}
ave_amplitude_dic = {}
ave_turnover_dic = {}
highest_price_dic = {}
lowest_price_dic = {}
#提取子表 
for i in range(1,101):
    number = 1000+i
    dfi = df[df['股票代码'] == number]
    #求和 并储存在字典中
    #以开盘价之和为例
    sum_open_price_dic[number] = '%.2f' % sum(dfi['开盘价'])
    sum_close_price_dic[number] ='%.2f' % sum(dfi['收盘价'])
    sum_highest_price_dic[number] ='%.2f' % sum(dfi['最高价'])
    sum_lowest_price_dic[number] ='%.2f' % sum(dfi['最低价'])
    sum_trade_volume_dic[number] ='%.2f' % sum(dfi['交易量'])
    sum_price_limit_dic[number] ='%.2f' % sum(dfi['涨跌幅'])
    sum_amplitude_dic[number] ='%.2f' % sum(dfi['振幅'])
    sum_turnover_dic[number] ='%.2f' % sum(dfi['换手率'])
    #求平均 并储存在字典中
    ave_open_price_dic[number] = '%.2f' % np.mean(dfi['开盘价'])
    ave_close_price_dic[number] ='%.2f' % np.mean(dfi['收盘价'])
    ave_highest_price_dic[number] ='%.2f' % np.mean(dfi['最高价'])
    ave_lowest_price_dic[number] ='%.2f' % np.mean(dfi['最低价'])
    ave_trade_volume_dic[number] ='%.2f' % np.mean(dfi['交易量'])
    ave_price_limit_dic[number] ='%.2f' % np.mean(dfi['涨跌幅'])
    ave_amplitude_dic[number] ='%.2f' % np.mean(dfi['振幅'])
    ave_turnover_dic[number] ='%.2f' % np.mean(dfi['换手率'])
    #求最高价
    highest_price_dic[number] = '%.2f' % max(dfi['最高价'])
    #求最低价
    lowest_price_dic[number] = '%.2f' % min(dfi['最低价'])
#导出
#example
df_sum_open_price = pd.DataFrame(list(sum_open_price_dic.items()), columns=['股票代码', '开盘价合计'])
df_sum_open_price.to_excel('开盘价合计', index=False)

#（二）数据可视化部分
#（1）开盘、收盘均值柱状图
#数据准备
x = np.arange(1001,1101)
width = 0.4
open_price_lis = list(map(float,ave_open_price_dic.values()))
close_price_lis = list(map(float,ave_close_price_dic.values()))
#图片绘制
plt.figure(figsize = (35,7))
plt.bar(x,open_price_lis,width,color = '#CD5555',label = '开盘价均值')
plt.bar(x+0.4,close_price_lis,width,color = '#4682B4',label = '收盘价均值')
plt.title('2021-01-04至2021-12-31期间100支股票的开盘价、收盘价均值柱状图')
plt.xlabel('股票代码')
plt.ylabel('价格（单位：元)')
plt.grid(axis = 'x')
plt.xticks((1001,1020,1040,1060,1080,1100))
plt.legend()
#图片导出
plt.savefig('图片1',dpi = 600)
#plt.show()
plt.close()

#（2）每支股票达到最高价的柱状图
#图片绘制
highest_price_lis = list(map(float,highest_price_dic.values()))
plt.figure(figsize = (35,7))
plt.bar(x,highest_price_lis,width,color ='#DB7093')
plt.title('2021-01-04至2021-12-31期间100支股票历史最高价柱状图')
plt.xlabel('股票代码')
plt.ylabel('价格（单位：元)')
plt.xticks((1001,1020,1040,1060,1080,1100))
plt.grid(axis = 'x')
#图片导出
plt.savefig('图片2',dpi = 600)
#plt.show()
plt.close()

#（3）每支股票达到的最低价的柱状图。
#图片绘制
lowest_price_lis = list(map(float,lowest_price_dic.values()))
plt.figure(figsize = (35,7))
plt.bar(x,lowest_price_lis,width,color ='#DB7093')
plt.title('2021-01-04至2021-12-31期间100支股票历史最低价柱状图')
plt.xlabel('股票代码')
plt.ylabel('价格（单位：元)')
plt.grid(axis = 'x')
plt.xticks((1001,1020,1040,1060,1080,1100))
#图片导出
plt.savefig('(图片3',dpi = 600)
plt.show()
plt.close()

#（4）每支股票当年的复合涨跌幅组成的柱状图。
#图片绘制
sum_price_lis = list(map(float,sum_price_limit_dic.values()))
plt.figure(figsize = (35,7))
plt.bar(x,sum_price_lis,width,color = '#B03060')
plt.title('2021-01-04至2021-12-31期间100支股票复合涨跌幅柱状图')
plt.xlabel('股票代码')
plt.ylabel('复合涨跌幅')
plt.grid(axis = 'x')
plt.xticks((1001,1020,1040,1060,1080,1100))
#图片导出
plt.savefig('图片4',dpi = 600)
plt.show()
plt.close()

#（5）每支股票的平均振幅组成的散点图。
#图片绘制
ave_amplitude_lis = list(map(float,ave_amplitude_dic.values()))
plt.figure(figsize = (35,7))
plt.scatter(x,ave_amplitude_lis,s = 20,c = 'g')
plt.xlabel('股票代码')
plt.ylabel('平均振幅')
plt.grid(axis = 'x')
plt.title('2021-01-04至2021-12-31期间100支股票平均振幅散点图')
plt.xticks((1001,1020,1040,1060,1080,1100))
#图片导出
plt.savefig('图片5',dpi = 600)
plt.show()
plt.close()

#（6）每支股票的平均换手率组成的柱状图
#图片绘制
ave_turnover_lis = list(map(float,ave_turnover_dic.values()))
plt.figure(figsize = (35,7))
plt.bar(x,ave_turnover_lis,width,color = '#8B0A50')
plt.xlabel('股票代码')
plt.ylabel('换手率')
plt.grid(axis = 'x')
plt.title('2021-01-04至2021-12-31期间100支股票平均换手率柱状图')
plt.xticks((1001,1020,1040,1060,1080,1100))
#图片导出
#plt.savefig('图片6')
plt.show()
plt.close()

#(7)总交易量柱状图
#图片绘制
sum_trade_volume_lis = list(map(float,sum_trade_volume_dic.values()))
plt.figure(figsize = (35,7))
plt.bar(x,sum_trade_volume_lis,width,color ='#8B0A50')
plt.title('2021-01-04至2021-12-31期间100支股票总交易量柱状图')
plt.xticks((1001,1020,1040,1060,1080,1100))
plt.xlabel('股票代码')
plt.ylabel('交易量')
plt.grid(axis = 'x')
#图片导出
plt.savefig('图片7',dpi = 600)
plt.show()
plt.close()


#TASK 2
for i in range(1,101):
    number = 1000+i
    dfi = df[df['股票代码'] == number]
    dfi_dates = dfi['日期']
    dfi_prices = dfi[['开盘价','收盘价']]
    days = []
    for index in list(dfi_dates.index):
        days.append(str(dfi_dates[index])[:11])
        days.append(str(dfi_dates[index])[:11])
    prices = []
    for j in range(len(list(dfi_prices.index))):
        prices.extend(list(dfi_prices.iloc[j]))
    #价格折线图
    fig,ax = plt.subplots(figsize = (35,7))
    ax.plot(days,prices,'r--',linewidth = 0.3)   
    ax.set_xlabel('时间')
    ax.set_ylabel('价格（单位：元）')
    ax.set_title(f'2021-01-04至2021-12-31期间代码为{number}的股票价格走势折线图')
    ax.grid(which = 'minor',axis = 'y')
    ax.xaxis.set_major_locator(ticker.MultipleLocator(40))
    plt.savefig(f'股票代码为{number}的图片1',dpi = 600)
    plt.show()
    plt.close()
    
 
  
    days = []
    for index in list(dfi_dates.index):
        days.append(str(dfi_dates[index])[:11])       
    #成交量柱状图
    fig,ax = plt.subplots(figsize = (35,7))
    ax.bar(days,dfi['交易量'],width = 0.4)
    ax.set_xlabel('时间')
    ax.set_ylabel('成交量')
    ax.set_title(f'2021-01-04至2021-12-31期间代码为{number}的股票成交量柱状图')
    ax.grid(which = 'minor',axis = 'y')
    ax.xaxis.set_major_locator(ticker.MultipleLocator(40))
    plt.savefig(f'股票代码为{number}的图片2',dpi = 600)
    plt.show()
    plt.close()
    
    #涨跌幅散点图
    fig,ax = plt.subplots(figsize = (35,7))
    my_color = ['#228B22' if i > 0 else '#A52A2A' for i in dfi['涨跌幅'].values]
    ax.scatter(days,dfi['涨跌幅'],s = 20,c = my_color)
    ax.set_xlabel('时间')
    ax.set_ylabel('涨跌幅')
    ax.set_title(f'2021-01-04至2021-12-31期间代码为{number}的股票涨跌幅散点图')
    ax.grid(which = 'minor',axis = 'y')
    ax.xaxis.set_major_locator(ticker.MultipleLocator(40))
    plt.savefig(f'股票代码为{number}的图片3',dpi = 600)
    plt.show()
    plt.close()  
    
 #振幅折线图   
    fig,ax = plt.subplots(figsize = (35,7)) 
    ax.plot(days,dfi['振幅'].values,c = '#8B658B')
    ax.set_xlabel('时间')
    ax.set_ylabel('振幅')
    ax.set_title(f'2021-01-04至2021-12-31期间代码为{number}的股票振幅折线图')
    ax.grid(which = 'minor',axis = 'y')
    ax.xaxis.set_major_locator(ticker.MultipleLocator(40))
    plt.savefig(f'股票代码为{number}的图片4',dpi = 600)
    plt.show()
    plt.close()
    
 #换手率柱状图
    fig,ax = plt.subplots(figsize = (35,7)) 
    ax.bar(days,dfi['换手率'].values,width = 0.4,color = '#FFB5C5')
    ax.set_xlabel('时间')
    ax.set_ylabel('换手率')
    ax.set_title(f'2021-01-04至2021-12-31期间代码为{number}的股票换手率柱状图')
    ax.grid(which = 'minor',axis = 'y')
    ax.xaxis.set_major_locator(ticker.MultipleLocator(40))
    plt.savefig(f'股票代码为{number}的图片5',dpi = 600)
    plt.show()
    plt.close()
    
    #if i == 1:
        #break

#移动平均线
for i in range(1,101):
    number = 1000+i
    #提取子表 设置x轴坐标（为在k线图中添加均线准备）
    dfi = df[df['股票代码'] == number]
    dfi_dates = dfi['日期']
    days = []
    for index in list(dfi_dates.index):
        days.append(str(dfi_dates[index])[:11])      
    # 修改索引、列名
    dfi.set_index(['日期'],inplace = True)
    dfi.index.name = 'Date'
    dfi.columns = ['Number','Open','Close','High','Low','Volume','Limit','Amplitude','Turnover']
    #计算5日均值、10日均值、30日均值 储存在dfi中
    dfi.loc[:,'mav5'] = dfi.loc[:,'Close'].rolling(window = 5).mean()
    dfi.loc[:,'mav10'] = dfi.loc[:,'Close'].rolling(window = 10).mean()
    dfi.loc[:,'mav30'] = dfi.loc[:,'Close'].rolling(window = 30).mean()
   #设置黄金均值点、死亡均值点条件
    golden_cross = (dfi['mav5'] > dfi['mav30']) & (dfi['mav5'].shift(1) <= dfi['mav30'].shift(1))
    death_cross = (dfi['mav5'] < dfi['mav30']) & (dfi['mav5'].shift(1) >= dfi['mav30'].shift(1))
    #找出黄金交叉点，死亡交叉点
    dfi['golden_cross'] = np.where(golden_cross, dfi['Close'], np.nan)
    dfi['death_cross'] = np.where(death_cross, dfi['Close'], np.nan)
    #画图准备
    add_plots = [(mpf.make_addplot(dfi['golden_cross'], type='scatter', markersize=100, marker='^', color='green')),    
              (mpf.make_addplot(dfi['death_cross'], type='scatter', markersize=100, marker='v', color='red'))]
    my_style = mpf.make_mpf_style(base_mpf_style='charles', mavcolors = ['red','green','blue'],rc={'font.family': 'SimHei', 'axes.unicode_minus': 'False'})
    #画图并保存图像
    fig,ax = mpf.plot(dfi,
         figsize = (35,7),
         type = 'line',
         addplot = add_plots,
         mav = (5,30),
         ylabel = '价格',
         title = f'2021-01-04至2021-12-31期间股票代码为{number}的移动平均线图',
         datetime_format='%Y-%m-%d',
         style = my_style,
         returnfig = True
         )
    ax[0].legend(['价格','5日移动平均线','30日移动平均线'])
    plt.savefig(f'股票代码{number}的图片6',dpi = 600)
    plt.show()
    plt.close()
    
#TASK 3 k线图
    fig,ax = mpf.plot(dfi,
                 type = 'candle',
                 figsize = (35,7),
                 style = my_style,
                 ylabel = '价格',
                 title = f'2021-01-04至2021-12-31期间股票代码为{number}的k线图',
                 volume = True,
                 ylabel_lower = '交易量',
                 returnfig = True)    
    ax[0].plot(days,dfi['mav5'],c = 'g',label = '5日均线')
    ax[0].plot(days,dfi['mav10'],c = 'r',label = '10日均线')
    ax[0].plot(days,dfi['mav30'],c = 'b',label = '30日均线')
    ax[0].legend()
    ax[0].xaxis.set_major_locator(ticker.MultipleLocator(40))
    plt.savefig(f'股票代码为{number}的图片7',dpi = 600)
    plt.show()
    plt.close()
    
    #if i == 1:
       #break



