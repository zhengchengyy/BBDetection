import socket
import threading
import socketserver
import json
import random
import time
import Adafruit_BBIO.ADC as ADC

def getVolt():
    ADC.setup()
    analogPin="P9_40"
    potVal=ADC.read(analogPin)
    potVolt=potVal*1.8
    time.sleep(0.01)  # 66次/s,不加它边存数据库和实时画图会有延迟
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
    configure_json = open("client.conf").read()
    conf = json.loads(configure_json)
    HOST,PORT = conf['host'],conf['port']
    NO = conf['device_no']
    while True:
        volt=getVolt()
        t = time.time()
        msg =[{
            "device_no":NO,
            "time": t,
            "voltage": volt
        }]
        jmsg = json.dumps(msg)
        client(HOST, PORT, jmsg)

