import pyformulas as pf
import socket
import threading
import socketserver
import json, types, string
import os, time
import matplotlib.pyplot as plt
import numpy as np
import math

# configurate the figure
import matplotlib as mpl
mpl.rc('lines', linewidth=1, color='r', linestyle='-')
plt.rcParams['figure.figsize'] = (10.0, 6.0)

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
        xs.append(x)
        ys.append(y)
        if len(xs) > 50:
            del xs[0]
            del ys[0]

    def handle(self):
        # transform original data
        data,addr = self.request[1].recvfrom(1024) #收到字节数组(bytes)数据，request[1]为socket
        str = data.decode('utf-8')  # 解码成utf-8格式的字符串
        dic = eval(str)[0] # 转换成字符串
        volt = dic['voltage']
        time = dic['time']
        # update data
        self.updateData(volt, time)
        global flag
        if (flag == False):
            # print(len(xs))
            fig = plt.figure()
            canvas = np.zeros((480, 640))
            screen = pf.screen(canvas, 'Examine')
            flag = True


        plt.ylim(0.4, 1.6)
        plt.xlim(xs[-1] - 20, xs[-1] + 2)
        plt.plot(xs, ys, c='blue')
        # if(flag == False):
        fig.canvas.draw()
            # flag = True
        image = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
        image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        screen.update(image)


        # print(len(xs))
        # print(volt,time)
        # self.plot();

    def plot(self):
        # canvas = np.zeros((480, 640))
        # screen = pf.screen(canvas, 'Examine')
        # plt.ylim(0.4, 1.6)
        while(True):
            print(len(xs))
            canvas = np.zeros((480, 640))
            screen = pf.screen(canvas, 'Examine')
            plt.ylim(0.4, 1.6)
            plt.xlim(xs[-1] - 20, xs[-1] + 2)
            plt.plot(xs, ys, c='blue')
            fig.canvas.draw()
            image = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
            image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
            screen.update(image)


class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass


if __name__ == "__main__":
    i = 0
    xs = [0]
    ys = [0]

    plt.ion()
    flag = False
    HOST, PORT = "", 20000
    server = ThreadedUDPServer((HOST, PORT), ThreadedUDPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    print("Server loop running in thread:", server_thread.name)
    print(" .... waiting for connection")
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()