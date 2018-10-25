from pymongo import MongoClient
from matplotlib import pyplot as plt
from matplotlib import style
from exceptions import *


def plot_from_db(action, db, volt_collection, tag_collection,port=27017, host='localhost', ndevices=3):
    client = MongoClient(port=port, host=host)
    database = client[db]
    tag_collection = database[tag_collection]
    volt_collection = database[volt_collection]

    if volt_collection.count_documents({}) + tag_collection.count_documents({}) < 2:
        raise CollectionError('Collection not found, please check names of the collection and database')

    ntags = tag_collection.count_documents({'tag':action})
    n = 1

    fig = plt.figure(figsize=(6,8))
    fig.suptitle(action)
    # plt.title(action)

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


        style.use('default')
        colors = ['r', 'b', 'g', 'c', 'k', 'p']
        base = ntags*100+10


        # plot
        ax = fig.add_subplot(base+n)
        n += 1
        for i in range(1, ndevices + 1):
            ax.plot(times[i], volts[i], label='device_' + str(i), color=colors[i - 1])
            ax.set_ylim([0,1.6])
            ax.set_ylabel('voltage')

        if n  == 2:
            ax.legend(loc='upper right')
        if n == ntags + 1:
            ax.set_xlabel('time')
        else:
            ax.set_xticks([])


    plt.show()

plot_from_db(action='lay',db='beaglebone',tag_collection='tags_4',volt_collection='volts_4')