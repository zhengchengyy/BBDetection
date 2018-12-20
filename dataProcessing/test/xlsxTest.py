from openpyxl import Workbook

workbook = Workbook()
booksheet = workbook.active  # 获取当前活跃的sheet,默认是第一个sheet
booksheet['A1'] = 'time'
booksheet['B1'] = 'volt_1'
booksheet['C1'] = 'volt_2'
booksheet['D1'] = 'volt_3'
for i in range(1,3):
	booksheet.cell(1,i).value = i

workbook.save("sample.xlsx")