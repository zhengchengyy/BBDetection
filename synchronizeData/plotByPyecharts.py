# 利用pyecharts库根据xlsx表格画图，最后输出html文件，可以通过浏览器访问图像
# coding:utf-8
# 导入读取Excel的库
import xlrd
from pyecharts import Bar
import numpy as np
#导入需要读取Excel表格的路径
filename = 'uneasy.xlsx'
picname = filename + '振动数据'
data = xlrd.open_workbook(r'C:\\Users\\Zheng Cheng\\Desktop\\'+filename)
table = data.sheets()[0]

y1=[]
y2=[]
y3=[]
x=[]

# 将列的值存入列表或者字符串
y1 = table.col_values(1)
y2 = table.col_values(2)#读取列的值
y3 = table.col_values(3)
x = table.col_values(4)

# 对第设备1数据进行平移处理，防止折线图重合
for i in range(1, len(y1)):
    y1[i]=float(y1[i])+0.2

bar=Bar(picname) #主副标题(主, 副)
# is_more_utils 为 True，提供更多实用工具按钮。
bar.add("volt_1",x,y1,is_more_utils=True,is_fill=True)#标题
bar.add("volt_2",x,y2,is_more_utils=True)
bar.add("volt_3",x,y3,is_more_utils=True)
bar.show_config()#展示HTML源代码

bar.render(r"C:/Users/Zheng Cheng/Desktop/"+filename+".html")#保存到本地bokezhexiantu.html
