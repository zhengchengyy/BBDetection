import socket
import time
import json
import Adafruit_BBIO.ADC as ADC


def sendWithDraw(NO, ip, port):
    ADC.setup()
    analogPin = "P9_40"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip_port = (ip, port)

    while True:
        potVal = ADC.read(analogPin)
        t = time.time()
        potVolt = potVal*1.8
        msg = {
            "device_no": NO,
            "time": t,
            "voltage": potVolt
        }
        sock.sendto(str(msg).encode("utf-8"), ip_port)
        time.sleep(0.01)


if __name__ == "__main__":
    configure_json = open("client.conf").read()
    conf = json.loads(configure_json)
    HOST, PORT = conf['host'], conf['port']
    NO = conf['device_no']
    sendWithDraw(NO, HOST, PORT)