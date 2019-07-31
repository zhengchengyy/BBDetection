# 直接读取mongodb数据中的数据存入表格，但是数据不同步，不进行插值处理，是dataSynchronization.py前半部分代码
# xlrd和xlwt处理的是xls文件，单个sheet最大行数是65535
# 该方法存入表格的数据量太小，弃用！！！
from pymongo import MongoClient
from exceptions import *
import xlwt


def save_to_excel(action, db, volt_collection, tag_collection,port=27017, host='localhost', ndevices=3):
    client = MongoClient(port=port, host=host)
    database = client[db]
    tag_collection = database[tag_collection]
    volt_collection = database[volt_collection]

    if volt_collection.count_documents({}) + tag_collection.count_documents({}) < 2:
        raise CollectionError('Collection not found, please check names of the collection and database')

    # save to excel
    excelfile = xlwt.Workbook(encoding='utf-8')
    table = excelfile.add_sheet('vibrate')
    table.write(0, 0, 'time')  # 写入数据table.write(行,列,value)
    table.write(0, 1, 'volt_1')
    table.write(0, 2, 'volt_2')
    table.write(0, 3, 'volt_3')
    # table.write(0, 4, 'heartRate')

    # plot the data that is of a certain action one by one
    for tag in tag_collection.find({'tag': action}):
        inittime, termtime = tag['inittime'], tag['termtime']

        # get the arrays according to which we will plot later
        times, volts = {}, {}
        for i in range(1, ndevices + 1):
            times[i] = []
            volts[i] = []

        for volt in volt_collection.find({'time': {'$gt': inittime,'$lt': termtime}}):
            device_no = int(volt['device_no'])
            v = volt['voltage']
            time = volt['time']
            times[device_no].append(time)
            volts[device_no].append(v)
            # print(times[device_no])

        for i in range(len(times[1])):
            table.write(i + 1, 0, str(times[1][i]))

        for col in range(1, ndevices + 1):
            for row in range(len(volts[col])):
                table.write(row + 1, col, str(volts[col][row]))

        excelfile.save(action + '.xls')

save_to_excel(action='easy',db='beaglebone',tag_collection='tags_5',volt_collection='volts_5')