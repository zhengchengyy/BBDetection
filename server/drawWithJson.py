from pymongo import MongoClient
from matplotlib import pyplot as plt
from matplotlib import style
import json
import time

'a simple example for drawing with .json file'

def timeToFormat(t):
    ftime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(t))
    return ftime

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

        fig = plt.figure(action, figsize=(6, 8))
        fig.suptitle(action)

        for data in tagData:
            initTime, termTime = data['inittime'], data["termtime"]
            # print(initTime,termTime)

            times, volts = {}, {}
            for i in range(1, ndevices + 1):
                times[i] = []
                volts[i] = []
            # I tried to use generator instead of list ,but I failed.
            # I don't know the exactly reason why generator can't work properly in a loop
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

            # plot, add_subplot(211)将画布分割成2行1列，图像画在从左到右从上到下的第1块
            ax = fig.add_subplot(base + n)
            ax.set_title(timeToFormat(initTime) + " ~ " + timeToFormat(termTime))
            ax.set_xlim(initTime, termTime)
            # 自定义y轴的区间，可以使图放大或者缩小
            # ax.set_ylim([0.8,1.8])
            ax.set_ylim([0.75, 0.90])
            # ax.set_ylim([0.81, 0.85])
            ax.set_ylabel('voltage')

            for i in range(1, ndevices + 1):
                # [v + i*0.2 for v in volts[i]]为了把多个设备的数据隔离开
                ax.plot(times[i], volts[i], label='device_' + str(i), color=colors[i - 1], alpha=0.9)

            if n == 1:
                ax.legend(loc='upper right')
            if n == ntags:
                ax.set_xlabel('time')
            n += 1

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
    # 大动作：翻身(turn_over)、腿部(hands_twitch)、伸展(legs_stretch)、手部伸展(hands_stretch)；
    # 小动作：腿部抽搐(legs_twitch)、手部抽搐(hands_twitch)、头部微小移动(head_move)；
    # 剧烈动作：抓握(grasp)、踢踹(kick)
    draw_with_json(
        "D:/Offer/BBDetection/data/tags_411.json",
        "D:/Offer/BBDetection/data/volts_411.json",
        'kick')