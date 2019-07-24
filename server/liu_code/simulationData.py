import socket
import random
import time


s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
    voltage = random.uniform(0, 1)
    t = time.time()
    data = {'voltage': voltage, 'time': t}
    s.sendto(str(data).encode('utf-8'), ('127.0.0.1', 20000))
    time.sleep(0.01)

