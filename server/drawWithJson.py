from pymongo import MongoClient
from matplotlib import pyplot as plt
from matplotlib import style
import json

'a simple example for drawing with .json file'

def draw_with_json(tag_url, volt_url, action, ndevices=3):
    tagData = []
    device_S = set()
    action_S = set()
    try:
        f_tag = open(tag_url, 'r')
        f_volt = open(volt_url, 'r')

        lines_tag = f_tag.readlines()
        lines_volt = f_volt.readlines()

        #The amount of voltage data is quite big, store them with a generator
        # volt_generater = (line for line in lines_volt)

        for line in lines_tag:
            #Turn the str to dict for the convinience of index after
            json_line = json.loads(line)

            #For future to cancel the parameter 'action'
            action_S.add(json_line['tag'])

            #List tagData store the whole data of the certain action
            if json_line['tag'] == action:
                tagData.append(json_line)

        # for line in lines_volt:
        #     json_line = json.loads(line)
        #     #For future to cancel the parameter 'ndevices'
        #     device_S.add(json_line['device_no'])

        ntags = len(tagData)
        n = 1

        fig = plt.figure(figsize=(6, 8))
        fig.suptitle(action)

        for data in tagData:
            initTime, termTime = data['inittime'], data["termtime"]
            print(initTime,termTime)

            times, volts = {}, {}
            for i in range(1, ndevices + 1):
                times[i] = []
                volts[i] = []
            # I tried to use generator instead of list ,but I failed.
            # I dont know the exactly reason why generator cant work properly in a loop
            # for i in volt_generater:
            #     json_i = json.loads(i)
            #     if (json_i['time'] <= termTime) and (json_i['time'] >= initTime):
            #         device_no = int(json_i['device_no'])
            #         v = json_i['voltage']
            #         time = json_i['time']
            #         times[device_no].append(time)
            #         volts[device_no].append(v)

            for i in lines_volt:
                json_i = json.loads(i)
                device_S.add(json_i['device_no'])
                if (json_i['time'] <= termTime) and (json_i['time'] >= initTime):
                    device_no = int(json_i['device_no'])
                    v = json_i['voltage']
                    time = json_i['time']
                    times[device_no].append(time)
                    volts[device_no].append(v)

            style.use('default')
            colors = ['r', 'b', 'g', 'c', 'k', 'p']
            base = ntags * 100 + 10

            ax = fig.add_subplot(base + n)
            n += 1
            for i in range(1, ndevices + 1):
                ax.plot(
                    times[i],
                    [v + i * 0.2 for v in volts[i]],
                    label='device_' + str(i),
                    color=colors[i - 1])
                ax.set_ylim([0.8,1.8])
                ax.set_ylabel('voltage')

            if n == 2:
                ax.legend(loc='upper right')
            if n == ntags + 1:
                ax.set_xlabel('time')
            else:
                ax.set_xticks([])

        plt.show()

    finally:
        if f_tag:
            f_tag.close()
        if f_volt:
            f_volt.close()

if __name__=='__main__':
    # First parameter:  the absolute path of tag.json
    # Second parameter: the absolute path of volt.json
    # Third parameter:  a certain action
    draw_with_json(
        "D:/Offer/BBDetection/data/tags_5.json",
        "D:/Offer/BBDetection/data/volts_5.json",
        'uneasy')
