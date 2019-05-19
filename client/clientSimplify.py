import socket
import json
import time
import Adafruit_BBIO.ADC as ADC


if __name__ == "__main__":
    configure_json = open("client.conf").read()
    conf = json.loads(configure_json)
    HOST,PORT = conf['host'],conf['port']
    No = conf['device_no']
    ADC.setup()
    analogPin = "P9_40"

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip_port = (HOST, PORT)
    while True:
        volt = ADC.read(analogPin)*1.8
        # time.sleep(0.01)
        t = time.time()
        msg =[{
            "device_no":No,
            "time": t,
            "voltage": volt
        }]
        jmsg = json.dumps(msg)
        sock.sendto(jmsg.encode("utf-8"), ip_port)
    sock.close()
