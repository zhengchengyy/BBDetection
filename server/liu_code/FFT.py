import time
import numpy as np
import Adafruit_BBIO.ADC as ADC
import queue
import threading

trsq = queue.Queue()
lock = threading.Lock()

def getVolt():
    ADC.setup()
    analogPin = "P9_40"
    while True:
        lock.acquire()
        potVal=ADC.read(analogPin)
        lock.release()
        t = time.time()
        potVolt=potVal*1.8
        msg = {
            "time": t,
            "voltage": potVolt
        }
        trsq.put(msg)
        time.sleep(0.01)

def FFTcaculate():
    dataList = []
    interval = 60
    while True:
        data = trsq.get()
        dataList.append(data)
        if data['time'] - dataList[0]['time'] >= interval:
            trueData = [i['voltage'] for i in dataList]
            lock.acquire()
            begin = time.time()
            result = np.fft.fft(trueData) / len(trueData)
            end = time.time()
            lock.release()
            print("result number:", len(result), 'cost time:', end-begin)
            dataList.clear()


if __name__ == "__main__":
    threading1 = threading.Thread(target=getVolt)
    threading2 = threading.Thread(target=FFTcaculate)
    threading1.setDaemon(True)
    threading2.setDaemon(True)
    threading1.start()
    threading2.start()
    threading1.join()
    threading2.join()

