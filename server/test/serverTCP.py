import pyformulas as pf
import socket
import threading
import socketserver
import json, types, string
import os, time
import matplotlib.pyplot as plt
import random
import numpy as np
import math

import matplotlib as mpl
mpl.rc('lines', linewidth=1, color='r', linestyle='-')
plt.rcParams['figure.figsize'] = (10.0, 6.0)

class PlotThread(threading.Thread):
    def __init__(self,xs,ys):
        super(PlotThread,self).__init__()
        self.xs = xs
        self.ys = ys
        self.xindicator = -1

    def run(self):
        fig = plt.figure()
        canvas = np.zeros((480, 640))
        screen = pf.screen(canvas, 'Examine')
        plt.ylim(-0.5,2)
        while True:
            threadLock.acquire()
            plt.xlim(xs[-1]-20,xs[-1]+2)
            plt.plot(self.xs, self.ys, c='blue')
            threadLock.release()

            # If we haven't already shown or saved the plot, then we need to draw the figure first...
            fig.canvas.draw()

            image = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
            image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))

            screen.update(image)
            time.sleep(0.01)



class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    #initiate the graph

    # fig, ax = plt.subplots()


    def __init__(self, request, client_address, server):
        self.request = request
        self.client_address = client_address
        self.server = server
        self.setup()
        try:
            self.handle()
        finally:
            self.finish()

    def updateData(self,x,y):
        threadLock.acquire()
        xs.append(x)
        ys.append(y)
        if len(xs) > 50:
            del xs[0]
            del ys[0]
        threadLock.release()

    def handle(self):
        #transform original data
        data = self.request.recv(1024)
        jdata = json.loads(data.decode('utf-8'))
        json_str = json.dumps(jdata[0])
        data2 = json.loads(json_str)
        volt = data2['voltage']
        time = data2['time']
        #update data
        self.updateData(time,volt)
        print(time,volt)
        # print(ys)



class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    # Port 0 means to select an arbitrary unused port
    HOST, PORT = "", 20000

    threadLock = threading.Lock()
    xs = [0]
    ys = [0]
    plotThread = PlotThread(xs,ys)
    plotThread.start()

    socketserver.TCPServer.allow_reuse_address = True
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    # server_thread.start()
    print("Server loop running in thread:", server_thread.name)
    print(" .... waiting for connection")

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()