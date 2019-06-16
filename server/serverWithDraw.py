import pyformulas as pf
import threading
import socketserver
import os
import matplotlib.pyplot as plt
import numpy as np


# configurate the figure
import matplotlib as mpl
mpl.rc('lines', linewidth=1, color='r', linestyle='-')
plt.rcParams['figure.figsize'] = (10.0, 6.0)


class PlotThread(threading.Thread):
    def __init__(self, xs, ys):
        super(PlotThread, self).__init__()
        self.xs = xs
        self.ys = ys
        self.xindicator = -1

    def run(self):
        fig = plt.figure()
        canvas = np.zeros((480, 640))
        screen = pf.screen(canvas, 'Examine')
        # plt.ylim(0.4, 1.6)
        plt.ylim(0.6, 1.0)
        # plt.ylim(-0.5, 2)
        # plt.ylim(0.695, 0.705)
        # plt.ylim(0.76, 0.77)
        # plt.ylim(1730, 1750)
        # plt.ylim(0.81,0.8125)
        while True:
            # threadLock.acquire()
            plt.xlim(xs[-1] - 20, xs[-1] + 2)
            plt.plot(self.xs, self.ys, c='blue')
            # threadLock.release()
            fig.canvas.draw()
            image = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
            image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
            screen.update(image)


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
        # threadLock.acquire()
        xs.append(x)
        ys.append(y)
        if len(xs) > 50:
            del xs[0]
            del ys[0]
            # xs.pop(0)
            # ys.pop(0)
        # threadLock.release()

    def handle(self):
        # transform original data
        data, addr = self.request[1].recvfrom(1024)  # 收到字节数组(bytes)数据，request[1]为socket
        str = data.decode('utf-8')  # 解码成utf-8格式的字符串
        dic = eval(str)[0]  # 转换成字典，eval()函数用来执行一个字符串表达式，并返回表达式的值。
        volt = dic['voltage']
        time = dic['time']
        # update data
        self.updateData(time, volt)


class ThreadedUDPServer(socketserver.ThreadingMixIn, socketserver.UDPServer):
    pass


if __name__ == "__main__":
    threadLock = threading.Lock()
    xs = [0]
    ys = [0]
    plotThread = PlotThread(xs, ys)
    plotThread.start()

    HOST, PORT = "", 20000
    server = ThreadedUDPServer((HOST, PORT), ThreadedUDPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    print("Server loop running in thread:", server_thread.name)
    print(" .... waiting for connection")
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()