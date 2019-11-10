import socket
import matplotlib.pyplot as plt
import threading
import time

RANGE = 300
IP2data = {}
filename = 'fileName.txt'
isStore = False


def collect():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('', 20000))
    tb = time.time()
    c = 0
    while True:
        data, _addr = s.recvfrom(7000)
        c += 1
        te = time.time()
        if te - tb > 1:
            print(c)
            tb = te
            c = 0
        data = eval(data.decode('utf-8'))

        if isStore:
            with open(filename, 'a') as f:
                f.write(str(data))
                f.write('\n')

        if IP2data.get(data['device_no']) == None:
            l = ([], [])
            IP2data[data['device_no']] = l
        IP2data[data['device_no']][0].append(data['time'])
        IP2data[data['device_no']][1].append(data['voltage'])
        if len(IP2data[data['device_no']][0]) > RANGE:
            IP2data[data['device_no']][0].pop(0)
            IP2data[data['device_no']][1].pop(0)


def drawer():
    while True:
        plt.clf()
        for i in IP2data.items():
            plt.plot(i[1][0], i[1][1], label=str(i[0]))
            plt.legend(loc=1, ncol=1)
        plt.ylim(0.8, 0.81)
        plt.pause(0.001)


thread1 = threading.Thread(target=collect)
thread2 = threading.Thread(target=drawer)
thread1.setDaemon(True)
thread2.setDaemon(True)
thread1.start()
if not isStore:
    thread2.start()
thread1.join()
if not isStore:
    thread2.join()
