import socket
import matplotlib.pyplot as plt
import threading

drawx = []
drawy = []
RANGE = 500
IP2data = {}


def collect():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.bind(('192.168.1.10', 20000))
    while True:
        data, addr = s.recvfrom(1024)
        if IP2data.get(addr[0]) == None:
            l = [[], []]
            IP2data[addr[0]] = l
        data = eval(data.decode('utf-8'))
        IP2data[addr[0]][0].append(data['time'])
        IP2data[addr[0]][1].append(data['voltage'])
        if len(IP2data[addr[0]][0]) > RANGE:
            IP2data[addr[0]][0].pop(0)
            IP2data[addr[0]][1].pop(0)


def drawer():
    while True:
        plt.clf()
        # x = IP2data['192.168.1.2'][0]
        for i in IP2data.values():
            plt.plot(i[0], i[1])
        plt.ylim(0.75, 0.85)
        plt.pause(0.001)


thread1 = threading.Thread(target=collect)
thread2 = threading.Thread(target=drawer)
thread1.setDaemon(True)
thread2.setDaemon(True)
thread1.start()
thread2.start()
thread1.join()
thread2.join()
