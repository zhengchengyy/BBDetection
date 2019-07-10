# coding:utf-8
from socket import *
from time import sleep
import json
import random
import Adafruit_BBIO.ADC as ADC
import time
import os
import threading
import SocketServer


# get volt
def getVolt():
    ADC.setup()
    analogPin = "P9_40"
    potVal = ADC.read(analogPin)
    potVolt = potVal * 1.8
    return potVolt


# alarm leds
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


def alarm(n):
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


def blink(n):
    LEDs = [SimpleLED(i) for i in range(4)]
    delay = 0.1
    for i in range(n):
        for j in range(4):
            LEDs[j].On()
        time.sleep(delay)
        for j in range(4):
            LEDs[j].Off()

        # TCP Server


class ThreadedTCPRequestHandler(SocketServer.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self.request = request
        self.client_address = client_address
        self.server = server
        self.setup()
        try:
            self.handle()
        finally:
            self.finish()

    def handle(self):
        counts = 0
        start_time = time.time()
        while True:
            self.request.setblocking(False)  # tcpCliSock设置成非阻塞
            try:
                receive_data = self.request.recv(1024)
            except:
                pass
            else:
                if not receive_data:
                    break
                print("receive:" + receive_data)
                blink(5)

            interval = time.time() - start_time
            volt = getVolt()
            if (volt > 0.9 or volt < 0.6) and volt > 0:
                counts = counts + 1
                send_data = str(interval) + "," + str(counts) + "e"
                self.request.send(send_data.encode("utf-8"))
                print("send:" + send_data)

    def setup(self):
        ip = self.client_address[0].strip()
        port = self.client_address[1]
        print(ip + ":" + str(port) + " is connecting!")


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


# UDP Server
class ThreadedUDPRequestHandler(SocketServer.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        self.request = request
        self.client_address = client_address
        self.server = server
        self.setup()
        try:
            self.handle()
        finally:
            self.finish()

    def handle(self):
        data = self.request[0]
        jdata = json.loads(data.decode('utf-8'))
        json_str = json.dumps(jdata[0])
        data2 = json.loads(json_str)
        volt = data2['voltage']
        time = data2['time']
        print(time, volt)

    def setup(self):
        ip = self.client_address[0].strip()
        port = self.client_address[1]
        print(ip + ":" + str(port) + " is connecting!")


class ThreadedUDPServer(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
    pass


if __name__ == "__main__":
    # TCP Server Thread
    # Port 0 means to select an arbitrary unused port
    TCP_HOST, TCP_PORT = "localhost", 7000
    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 7000
    tcp_server = ThreadedTCPServer((TCP_HOST, TCP_PORT), ThreadedTCPRequestHandler)
    # Start a thread with the server -- that thread will then start one
    tcp_server_thread = threading.Thread(target=tcp_server.serve_forever)
    # Exit the server thread when the main thread terminates
    tcp_server_thread.daemon = True
    tcp_server_thread.start()
    print("TCP Server loop running in thread:", tcp_server_thread.name)
    print(" .... waiting for connection")
    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C

    # UDP Server Thread
    UDP_HOST, UDP_PORT = "", 20000
    server = ThreadedUDPServer((UDP_HOST, UDP_PORT), ThreadedUDPRequestHandler)
    udp_server_thread = threading.Thread(target=server.serve_forever)
    udp_server_thread.daemon = True
    udp_server_thread.start()
    print("UDP Server loop running in thread:", udp_server_thread.name)
    print(" .... waiting for connection")

    # Always process requests
    tcp_server.serve_forever()
    udp_server.serve_forever()
