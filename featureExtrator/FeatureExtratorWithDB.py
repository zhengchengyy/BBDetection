from feature_modules import *
from feature_extractor import FeatureExtractor
import time

from pymongo import MongoClient
from exceptions import CollectionError
from pymongo import MongoClient

config = {'action':'legs_stretch',
          'db':'beaglebone',
          'tag_collection':'tags_517',
          'volt_collection':'volts_517'}

def read_from_db(action, db, volt_collection, tag_collection,port=27017, host='localhost', ndevices=5):
    client = MongoClient(port=port, host=host)
    database = client[db]
    tag_collection = database[tag_collection]
    volt_collection = database[volt_collection]

    try:
        if volt_collection.count_documents({}) + tag_collection.count_documents({}) < 2:
            raise CollectionError('Collection not found, please check names of the collection and database')
    except CollectionError as e:
        print(e.message)

    ntags = tag_collection.count_documents({'tag':action})

    # read the data that is of a certain action one by one
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

    return times,volts


if __name__=='__main__':
    times, volts = read_from_db(action=config['action'],
                                db=config['db'],
                                tag_collection=config['tag_collection'],
                                volt_collection=config['volt_collection'])

    # 根据时间采集数据，基本单位为s，比如1s、10s、30s、60s
    # interval表示每次分析的时间跨度，rate表示间隔多长时间进行一次分析
    interval = 1
    rate = 1

    # 定义特征提取器
    extractor = FeatureExtractor()

    # 定义特征提取模块
    variancemodule = VarianceModule(interval, rate)
    averagemodule = AverageModule(interval, rate)
    thresholdcounter = ThresholdCounterModule(interval, rate)

    # 注册特征提取模块
    extractor.register(variancemodule)
    extractor.register(averagemodule)
    extractor.register(thresholdcounter)

    # 启动Mongo客户端
    client = MongoClient()
    db = client.beaglebone
    collection = db.features_411

    # 定义设备数
    ndevices = 5

    # 对每个采集设备进行特征提取
    for i in range(1, ndevices + 1):
        for j in range(len(volts[i])):
            value = {
                "time" : times[i][j],
                "volt" : volts[i][j]
            }
            output = extractor.process(value)
            if (output):
                features = {
                    "device_no": i,
                    "time": times[i][j],
                    "features": output,
                    "interval": interval,
                    "rate": rate
                }
                print(features)
                # 把特征数据存入数据库
                # collection.insert_one(features)

        # 清理所有模块，防止过期数据
        extractor.clear()
    
