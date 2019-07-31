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
          'volt_collection':'volts_411',
          'offset':0}

def timeToFormat(t):
    ftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
    return ftime

def timeToSecond(t):
    stime = time.strftime("%M:%S", time.localtime(t))
    return stime

def draw_features_from_db(action, db, volt_collection, tag_collection,port=27017, host='localhost', ndevices=3, offset=0):
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

    title = config['volt_collection'][6:] + "" + action + "_features"
    fig = plt.figure(title, figsize=(6, 8))
    fig.suptitle(action)

    # 根据时间采集数据，基本单位为s，比如1s、10s、30s、60s
    # interval表示每次分析的时间跨度，rate表示间隔多长时间进行一次分析
    interval = 1
    rate = 1

    # 定义特征提取器
    extractor = FeatureExtractor()

    # 定义特征提取模块
    rangemodule = RangeModule(interval, rate)
    vibrationfreq = VibrationFreqModule(interval, rate)
    thresholdcounter = ThresholdCounterModule(interval, rate)

    # 注册特征提取模块
    extractor.register(rangemodule)
    extractor.register(vibrationfreq)
    extractor.register(thresholdcounter)

    # 定义画布左右位置的计数：标签累加，即人数累加
    tag_acc = 1

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

        # 定义存储时间、特征列表
        feature_times, feature_values = {}, {}
        for i in range(1, ndevices + 1):
            feature_times[i] = []
            feature_values[i] = {'Range': [], 'VibrationFreq': [], 'ThresholdCounter': []}

        # 对每个采集设备进行特征提取
        for i in range(1, ndevices + 1):
            for j in range(len(volts[i])):
                value = {
                    "time": times[i][j],
                    "volt": volts[i][j]
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

            # 清理所有模块，防止过期数据
            extractor.clear()

        # 定义特征数量
        nfeatures = 3
        # 定义画布上下位置的计数，即特征累加
        fea_acc = 1
        base = nfeatures * 100 + ntags*10
        style.use('default')
        colors = ['r', 'b', 'g', 'c', 'm']  # m c
        # subtitle = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
        # fig.suptitle("Person" + subtitle[tag_acc - 1] + ": " + timeToFormat(inittime + offset)
        #              + " ~ " + timeToFormat(termtime + offset))


        for feature_type in feature_values[1].keys():
            # plot, add_subplot(311)将画布分割成3行1列，图像画在从左到右从上到下的第1块
            ax = fig.add_subplot(base + tag_acc + (fea_acc-1) * ntags)
            plt.subplots_adjust(hspace=0.5)  # 函数中的wspace是子图之间的垂直间距，hspace是子图的上下间距
            ax.set_title(feature_type)

            for i in range(1, ndevices + 1):
                ax.set_xlim(feature_times[i][0], feature_times[i][-1])
                ax.plot(feature_times[i], feature_values[i][feature_type],
                        label='device_' + str(i), color=colors[i - 1], alpha=0.9)

            # 设置每个数据对应的图像名称
            if fea_acc == 1 and tag_acc == 2:
                ax.legend(loc='best')
            if fea_acc == nfeatures:
                ax.set_xlabel('Time')
            fea_acc += 1

            # 以第一个设备的时间数据为准，数据的每1/10添加一个x轴标签
            xticks = []
            xticklabels = []
            length = len(feature_times[1])
            interval = length // 10 - 1
            for i in range(0, length, interval):
                xticks.append(feature_times[1][i])
                xticklabels.append(timeToSecond(feature_times[1][i] + offset))
            ax.set_xticks(xticks)  # 设定标签的实际数字，数据类型必须和原数据一致
            ax.set_xticklabels(xticklabels, rotation=15)  # 设定我们希望它显示的结果，xticks和xticklabels的元素一一对应

        tag_acc += 1

    plt.show()


if __name__=='__main__':
    draw_features_from_db(action=config['action'],
                                db=config['db'],
                                tag_collection=config['tag_collection'],
                                volt_collection=config['volt_collection'],
                                offset=config['offset'])