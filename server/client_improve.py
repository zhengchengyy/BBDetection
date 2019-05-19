import socket
import threading
import json
import time
import Adafruit_BBIO.ADC as ADC
import queue

trsq = queue.Queue()

def getVolt(NO):
    while True:
        ADC.setup()
        analogPin="P9_40"
        potVal=ADC.read(analogPin)
        t = time.time()
        potVolt=potVal*1.8
        msg = {
            "device_no": NO,
            "time": t,
            "voltage": potVal
        }
        trsq.put(msg)
        time.sleep(0.01)


def client(ip, port, interval):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip_port = (ip, port)
    sendData = []
    while True:
        data = trsq.get()
        sendData.append(data)
        if data['time'] - sendData[0]['time'] >= interval:
            # try:
                print ("Send size: {}".format(len(str(sendData).encode("utf-8"))))
                sock.sendto(str(sendData).encode("utf-8"),ip_port)
                sendData.clear()
            # finally:
            #     sock.close()

if __name__ == "__main__":
    configure_json = open("client.conf").read()
    conf = json.loads(configure_json)
    HOST,PORT = conf['host'],conf['port']
    NO = conf['device_no']
    # while True:
    #     volt=getVolt()
    #     t = time.time()
    #     msg =[{
    #         "device_no":NO,
    #         "time": t,
    #         "voltage": volt
    #     }]
    #     jmsg = json.dumps(msg)
    #     client(HOST, PORT, jmsg)
    produce = threading.Thread(target = getVolt, args = (NO,))
    produce.setDaemon(True)
    send = threading.Thread(target = client, args = (HOST, PORT, 1))
    send.setDaemon(True)
    produce.start()
    send.start()
    produce.join()
    send.join()

