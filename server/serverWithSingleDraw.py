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
        self.updateData(volt, time)
        self.plot()

        # ax.cla()
        # ax.bar(ys, label='test', height=ys, width=0.3)
        # ax.legend()
        # plt.pause(0.3)



    def plot(self):

        plt.clf()
        plt.plot(xs,ys)
        plt.show()
        # while(True):
        #     print(len(xs), len(ys))
        #     fig = plt.figure()
        #     canvas = np.zeros((480, 640))
        #     screen = pf.screen(canvas, 'Examine')
        #     plt.ylim(0.4, 1.6)
        #     plt.xlim(xs[-1] - 20, xs[-1] + 2)
        #     plt.plot(xs, ys, c='blue')
        #     fig.canvas.draw()
        #     image = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
        #     image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        #     screen.update(image)

class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass


if __name__ == "__main__":
    i = 0
    xs = [0]
    ys = [0]

    plt.ion()

    HOST, PORT = "", 20000
    server = ThreadedUDPServer((HOST, PORT), ThreadedUDPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    print("Server loop running in thread:", server_thread.name)
    print(" .... waiting for connection")
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()