# -*- coding: utf-8 -*-

'''将原本的clinetWithAll改变为使用多线程启动，应用生产者消费者模型
将获取电压值与处理电压值由串行执行改变为并行执行，提升程序速度
新增以及改变的代码均使用两行------标识'''


# 首先从传感器获取电压值；然后对这些电压值进行特征提取，比如超过某个阈值的次数可以表示翻身次数；
# 再把特征数据传给推理机，推理把推理结果返回，根据返回值判断睡眠状态，进而采取相应措施，比如闪烁报警。

# 导入基本模块
import socket
import socketserver
import json
import time
import os
import Adafruit_BBIO.ADC as ADC

#添加队列模块，用于传递生产者消费者之间数据
#添加多线程模块
#-----
from queue import Queue
import threading
#-----


#现修改为按照时间操作的模块
#------
# 导入特征提取模块
from feature_modules_improve import *
from feature_extractor_improve import FeatureExtractor
#------

# 导入推理机模块，使用动态链接库
from ctypes import *

#实例化传递数据的队列
#设定每秒采集的数据量，用于决定特征提取器的队列长度
#------
dataQueue = Queue(maxsize = 1000)
#CPS变量在改变为按时间操作后，不再需要
#CPS = 75
#------

#设定进行特征处理的处理模块
#修改为适应时间操作
#-------
def getExtractor(interval = 1, rate = 0.5):

    # 定义特征提取器
    extractor = FeatureExtractor()

    # 定义特征提取模块
    thresholdcounter = ThresholdCounterModule(interval, rate)

    # 注册特征提取模块
    extractor.register(thresholdcounter)

    return extractor
#-------


#生产者线程函数
#------
def sendVoltToQueue(NO,HOST,PORT):
    while True:
        volt = getVolt()
        t = time.time()
        msg = [{
            "device_no": NO,
            "time": t,
            "voltage": volt
        }]
        jmsg = json.dumps(msg)
        dataQueue.put({'volt' : volt, 'time' : t})
        client(HOST,PORT, jmsg)
#------


#消费者线程
#------
def processQueueData():
    interval = 8
    rate = 1
    extractor = getExtractor(interval, rate)
    while True:
        d = dataQueue.get()
        #为适应按时间处理，此处传入的数据应该为d本身,而不仅仅是电压
        #output = extractor.process(d['volt'])
        output = extractor.process(d)
        if (output or output == 0):
            features = {
                "device_no": NO,
                "time": d['time'],
                "feature_value": output,
                "interval": interval
            }
            # print(features)

            counts = output.get("ThresholdCounter")
            print("counts：", counts)

            # 1 初始化推理机
            libtest = cdll.LoadLibrary("./libtest.so")
            libtest.initReasonging()

            # 2 设置参数，注意python2的字符串默认为bytes，而python3的字符串为unicode编码
            libtest.setParaValue("counts".encode("utf-8"), c_double(counts))

            # 3 启动推理机
            libtest.startReasoning()

            # 4 获取参数值
            PygetParaValue = libtest.getParaValue
            PygetParaValue.restype = c_double  # 默认返回int类型，restype设置函数的返回类型
            sleep = PygetParaValue("sleep".encode("utf-8"))
            if(sleep==-1.0):
                blink(1)
            if(sleep==-2.0):
                alarm(3)
            # time.sleep(1)
            print("sleep：", sleep)

            # 5 释放内存
            libtest.endReasoning()
#------

# 获取电压值
def getVolt():
    ADC.setup()
    analogPin="P9_40"
    potVal=ADC.read(analogPin)
    potVolt=potVal*1.8
    time.sleep(0.01)  # 66次/s,不加它边存数据库和实时画图会有延迟
    return potVolt

# 创建客户端
def client(ip, port,message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # print ("Send: {}".format(message))
        ip_port = (ip,port)
        sock.sendto(message.encode('utf-8'),ip_port)
    finally:
        sock.close()

# 初始化警报灯
class SimpleLED:
    def __init__(self, led_no):
        self.led_no = led_no
        self.led_path = "/sys/class/leds/beaglebone:green:usr%d/" % self.led_no
        os.system("echo none > %strigger" % self.led_path)
        self.state = "off"

    def On(self):
        if self.state != "on":
            os.system("echo 1 > %sbrightness" % self.led_path)
            self.state = "on"

    def Off(self):
        if self.state != "off":
            os.system("echo 0 > %sbrightness" % self.led_path)
            self.state = "off"

# 轻微报警(跑马灯)
def blink(n):
    LEDs = [SimpleLED(i) for i in range(4)]
    delay = 0.1
    for i in range(n):
        for j in range(4):
            LEDs[j].On()
            time.sleep(delay)
        time.sleep(delay)
        for j in range(4):
            LEDs[j].Off()
        time.sleep(delay)

# 严重报警(快速闪烁)
def alarm(n):
    LEDs = [SimpleLED(i) for i in range(4)]
    delay = 0.1
    for i in range(n):
        for j in range(4):
            LEDs[j].On()
        time.sleep(delay)
        for j in range(4):
            LEDs[j].Off()

if __name__ == "__main__":
    # 读取配置文件，设置主机地址和端口号
    configure_json = open("client.conf").read()
    conf = json.loads(configure_json)
    HOST,PORT = conf['host'],conf['port']
    NO = conf['device_no']

#使用多线程完成被注释功能
#------
    producer = threading.Thread(target = sendVoltToQueue, name = 'getVolt',args=(NO,HOST,PORT))
    consumer = threading.Thread(target = processQueueData, name = 'handleVoltData')
    producer.setDaemon(True)
    consumer.setDaemon(True)
    producer.start()
    consumer.start()
    producer.join()
    consumer.join()
#------

#以下代码改变为采用多线程实现
'''
    # 配置队列信息，maxsize表示队列最大长度，leapsize表示每次移动长度
    # 根据时间采集数据，基本单位为s，比如一分钟，十分钟，75次/s
    interval = 1
    maxsize = 75 * interval
    leapsize = 74

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

    while True:
        volt = getVolt()
        t = time.time()

        output = extractor.process(volt)
        if (output or output == 0):
            features = {
                "device_no": NO,
                "time": t,
                "feature_value": output,
                "interval": interval
            }
            # print(features)

            counts = output.get("ThresholdCounter")
            print("counts：", counts)

            # 1 初始化推理机
            libtest = cdll.LoadLibrary("./libtest.so")
            libtest.initReasonging()

            # 2 设置参数，注意python2的字符串默认为bytes，而python3的字符串为unicode编码
            libtest.setParaValue("counts".encode("utf-8"), c_double(counts))

            # 3 启动推理机
            libtest.startReasoning()

            # 4 获取参数值
            PygetParaValue = libtest.getParaValue
            PygetParaValue.restype = c_double  # 默认返回int类型，restype设置函数的返回类型
            sleep = PygetParaValue("sleep".encode("utf-8"))
            if(sleep==-1.0):
                blink(1)
            if(sleep==-2.0):
                alarm(3)
            # time.sleep(1)
            print("sleep：", sleep)

            # 5 释放内存
            libtest.endReasoning()

        # jmsg = json.dumps(msg)
        # client(HOST, PORT, jmsg)
'''