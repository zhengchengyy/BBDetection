from openpyxl import load_workbook
from openpyxl import Workbook
import time, datetime

workbook = load_workbook('uneasy.xlsx')
sheets = workbook.get_sheet_names()  # 从名称获取sheet
booksheet = workbook.get_sheet_by_name(sheets[0])  #取第一张表

# input parameter timeStamp must be int type
def timeStampToTime(timeStamp):
	timeArray = time.localtime(timeStamp)
	otherStyleTime = time.strftime("%H:%M:%S", timeArray)
	return otherStyleTime

str = "1543136196.4364"
stamp = float(str)
print(type(stamp),stamp)
print(timeStampToTime(float(str)))