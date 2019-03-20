from feature_modules import *
from feature_extractor import FeatureExtractor

import socket
import threading
import socketserver
import json, types, string
import os, time

from ctypes import *

class FeatureExtract(threading.Thread):
    def __init__(self, times, volts):
        super(FeatureExtract, self).__init__()
        self.times = times
        self.volts = volts
        self.xindicator = -1

    def run(self):

        # 配置队列信息，maxsize表示队列最大长度，leapsize表示每次移动长度
        # 根据时间采集数据，基本单位为s，比如一分钟，十分钟，75次/s
        interval = 1
        maxsize = 75 * interval
        leapsize = 1

        # 定义特征提取器
        extractor = FeatureExtractor()

        # 定义特征提取模块
        variancemodule = VarianceModule(maxsize, leapsize)
        averagemodule = AverageModule(maxsize, leapsize)
        thresholdcounter = ThresholdCounterModule(maxsize, leapsize)

        # 注册特征提取模块
        # extractor.register(variancemodule)
        # extractor.register(averagemodule)
        extractor.register(thresholdcounter)

        i = 0
        while True:
            while(i<len(volts)):
                deviceNo = 2
                output = extractor.process(volts[i])
                t = times[i]
                i = i + 1

                if(output or output==0):
                    features = {
                        "device_no": deviceNo,
                        "time": t,
                        "feature_value": output,
                        "interval": interval
                    }
                    print(features)
                    # print(output.get("ThresholdCounter"))
                    # counts = output.get("ThresholdCounter")


class ThreadedUDPRequestHandler(socketserver.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self.request = request
        self.client_address = client_address
        self.server = server
        try:
            self.handle()
        finally:
            self.finish()

    def updateData(self, x, y):
        threadLock.acquire()
        times.append(x)
        volts.append(y)
        threadLock.release()

    def handle(self):
        # transform original data
        data = self.request[0]
        jdata = json.loads(data.decode('utf-8'))
        # print(jdata)
        json_str = json.dumps(jdata[0])
        data2 = json.loads(json_str)
        # prevent abnormal data
        # if data2['voltage']>0.5 and data2['voltage']<1.2:
        volt = data2['voltage']
        time = data2['time']
        # update data
        self.updateData(time, volt)
        # print(time, volt)


class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass


if __name__ == "__main__":
    threadLock = threading.Lock()
    times = [0]
    volts = [0]
    featureExtract = FeatureExtract(times, volts)
    featureExtract.start()

    HOST, PORT = "", 20000
    server = ThreadedUDPServer((HOST, PORT), ThreadedUDPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    print("Server loop running in thread:", server_thread.name)
    print(" .... waiting for connection")
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()