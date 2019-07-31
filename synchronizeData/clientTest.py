import socket
import threading
import socketserver
import json
import random
import time
import Adafruit_BBIO.ADC as ADC

def getVolt():
    ADC.setup()
    from time import sleep
    analogPin="P9_40"
    potVal=ADC.read(analogPin)
    potVolt=potVal*1.8
    sleep(0.01)
    return potVolt

def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        print ("Send: {}".format(message))
        ip_port = (ip,port)
        sock.sendto(message.encode("utf-8"),ip_port)
    finally:
        sock.close()

if __name__ == "__main__":
    HOST, PORT = "", 20000
    while True:
        volt=getVolt()
        t = time.time()
        msg =[{
            "time": t,
            "voltage": volt
        }]
        jmsg = json.dumps(msg)
        client(HOST, PORT, jmsg)
