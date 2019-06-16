import time
import ntplib

haomiao = lambda t : int(round(t * 100)) % 100
c = ntplib.NTPClient()
response = c.request('192.168.1.2')
ts = response.tx_time
thisPC = time.time()
print("ntp server time:",ts)
print("this PC time:", thisPC)
print("offset:", thisPC - ts)
# h = haomiao(ts)
# _date = time.strftime('%Y/%m/%d',time.localtime(ts))
# print(_date)
# _time = time.strftime('%X',time.localtime(ts))
# print(_time)
# print('date {0} && time {1}.{2}'.format(_date,_time,h))

# ntp server time: 1463874631.6392817
# this PC time: 1558097897.627403
# offset: 94223265.98812127

# ntp server time: 1463906029.6658
# this PC time: 1560519170.621749
# offset: 96613140.95594883