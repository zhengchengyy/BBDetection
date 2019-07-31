from feature_modules import *
from feature_extractor import FeatureExtractor
import time

from pymongo import MongoClient
from exceptions import CollectionError
from pymongo import MongoClient

from matplotlib import pyplot as plt
from matplotlib import style

config = {'action': 'turn_over',
          'db': 'beaglebone',
          'tag_collection': 'tags_411',
          'volt_collection': 'volts_411'}


def read_from_db(action, db, volt_collection, tag_collection, port=27017, host='localhost', ndevices=5):
    client = MongoClient(port=port, host=host)
    database = client[db]
    tag_collection = database[tag_collection]
    volt_collection = database[volt_collection]

    try:
        if volt_collection.count_documents({}) + tag_collection.count_documents({}) < 2:
            raise CollectionError('Collection not found, please check names of the collection and database')
    except CollectionError as e:
        print(e.message)

    ntags = tag_collection.count_documents({'tag': action})

    # read the data that is of a certain action one by one
    for tag in tag_collection.find({'tag': action}):
        inittime, termtime = tag['inittime'], tag['termtime']

        # get the arrays according to which we will plot later
        times, volts = {}, {}
        for i in range(1, ndevices + 1):
            times[i] = []
            volts[i] = []

        for volt in volt_collection.find({'time': {'$gt': inittime, '$lt': termtime}}):
            device_no = int(volt['device_no'])
            v = volt['voltage']
            time = volt['time']
            times[device_no].append(time)
            volts[device_no].append(v)

    return times, volts


if __name__ == '__main__':
    times, volts = read_from_db(action=config['action'],
                                db=config['db'],
                                tag_collection=config['tag_collection'],
                                volt_collection=config['volt_collection'])

    # 根据时间采集数据，基本单位为s，比如1s、10s、30s、60s
    # interval表示每次分析的时间跨度，rate表示间隔多长时间进行一次分析
    interval = 2
    rate = 2

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

    # 定义存储特征列表
    features = {}
    for i in range(1, ndevices + 1):
        features[i] = []

    # 对每个采集设备进行特征提取
    for i in range(1, ndevices + 1):
        for j in range(len(volts[i])):
            value = {
                "time": times[i][j],
                "volt": volts[i][j]
            }
            output = extractor.process(value)
            if (output):
                feature = {
                    # "device_no": i,
                    "feature_time": times[i][j],
                    "feature_value": output['Variance'],
                    # "interval": interval,
                    # "rate": rate
                }
                # print(feature)
                features[i].append(feature)
                # 把特征数据存入数据库
                # collection.insert_one(features)

        # 清理组件
        variancemodule.clear()
        averagemodule.clear()
        thresholdcounter.clear()

    title = "features"
    fig = plt.figure(title, figsize=(6, 8))
    fig.suptitle("feature")

    feature_count = 3
    n = 1

    style.use('default')
    colors = ['r', 'b', 'g', 'c', 'm']  # m c
    subtitle = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    # base = feature_count * 100 + 10

    # plot, add_subplot(211)将画布分割成2行1列，图像画在从左到右从上到下的第1块
    # ax = fig.add_subplot(base + n)
    # plt.subplots_adjust(hspace=0.5)  # 函数中的wspace是子图之间的垂直间距，hspace是子图的上下间距
    # ax.set_xlim(inittime, termtime)

    # 定义存储时间、特征列表
    feature_times, feature_values = {}, {}
    for i in range(1, ndevices + 1):
        feature_times[i] = []
        feature_values[i] = []
    for i in range(1, len(features)+1):
        for j in range(len(features[i])):
            feature_times[i].append(features[i][j]['feature_time'])
            feature_values[i].append(features[i][j]['feature_value'])

    # print(feature_values)
    # print(feature_times)
    for i in range(1, ndevices + 1):
        plt.plot(feature_times[i], feature_values[i], label='device_' + str(i), color=colors[i - 1], alpha=0.9)
    plt.show()