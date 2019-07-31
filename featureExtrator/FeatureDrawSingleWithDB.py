from feature_modules import *
from feature_extractor import FeatureExtractor
import time

from pymongo import MongoClient
from exceptions import CollectionError
from pymongo import MongoClient

from matplotlib import pyplot as plt
from matplotlib import style

config = {'action':'turn_over',
          'db':'beaglebone',
          'tag_collection':'tags_411',
          'volt_collection':'volts_411'}

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

def draw_from_data(feature_type, feature_time, feature_values, ndevices=5):
    style.use('default')
    colors = ['r', 'b', 'g', 'c', 'm']  # m c
    for i in range(1, ndevices + 1):
        plt.plot(feature_times[i], feature_values[i]['Variance'], label='device_' + str(i), color=colors[i - 1],
                 alpha=0.9)
    plt.show()


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
    rangemodule = RangeModule(interval, rate)
    averagemodule = AverageModule(interval, rate)
    samplingcounter = SamplingCounterModule(interval, rate)

    # 注册特征提取模块
    extractor.register(rangemodule)
    extractor.register(averagemodule)
    extractor.register(samplingcounter)

    # 启动Mongo客户端
    client = MongoClient()
    db = client.beaglebone
    collection = db.features_411

    # 定义设备数
    ndevices = 5

    # 定义特征数量
    nfeatures = 3

    # 定义存储时间、特征列表
    feature_times, feature_values = {}, {}
    for i in range(1, ndevices + 1):
        feature_times[i] = []
        feature_values[i] = {'Range':[],'Average':[],'SamplingCounter':[]}

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
                    "feature_time": times[i][j],
                    "feature_value": output,
                    "interval": interval,
                    "rate": rate
                }
                feature_times[i].append(features['feature_time'])
                for feature_type in feature_values[i].keys():
                    feature_values[i][feature_type].append(features['feature_value'][feature_type])

                # 把特征数据存入数据库
                # collection.insert_one(features)

        # 清理所有模块，防止过期数据
        extractor.clear()

    title = config['volt_collection'][6:] + "" + config['action']
    fig = plt.figure(title, figsize=(6, 8))
    fig.suptitle("features")

    # 定义画布位置的计数
    n = 1

    for feature_type in feature_values[1].keys():
        style.use('default')
        colors = ['r', 'b', 'g', 'c', 'm']  # m c
        base = nfeatures * 100 + 10
        # plot, add_subplot(211)将画布分割成2行1列，图像画在从左到右从上到下的第1块
        ax = fig.add_subplot(base + n)
        plt.subplots_adjust(hspace=0.5)  # 函数中的wspace是子图之间的垂直间距，hspace是子图的上下间距
        ax.set_title(feature_type)
        # ax.set_xlim(inittime, termtime)

        for i in range(1, ndevices + 1):
            ax.plot(feature_times[i], feature_values[i][feature_type],
                    label='device_' + str(i), color=colors[i - 1], alpha=0.9)

        if n  == 1:
            ax.legend(loc='upper right')
        if n == nfeatures:
            ax.set_xlabel('Time')
        n += 1

    plt.show()