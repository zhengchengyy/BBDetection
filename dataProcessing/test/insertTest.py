times, volts = {}, {}
ndevices = 3
for i in range(1, ndevices+1):
    times[i] = []
    volts[i] = []
times[1]=[1,2,4,9]
times[2]=[6,10]
times[3]=[3,4,5]
volts[1]=[1.13,1.21,1.51,1,41]
volts[2]=[1.31,1.21]
volts[3]=[1.11,1.21,1.32]

# 合并两个设备的有序时间列表
def merge(time1,time2):
    res_time = []
    p = 0
    q = 0
    while p!=len(time1) and q!=len(time2):
        if time1[p]==time2[q]:
            res_time.append(time1[p])
            p = p+1
            q = q+1
        elif time1[p]<time2[q]:
            res_time.append(time1[p])
            p = p+1
        else:
            res_time.append(time2[q])
            q = q+1

    while p!=len(time1):
        res_time.append(time1[p])
        p = p + 1

    while q!=len(time2):
        res_time.append(time2[q])
        q = q + 1
    return res_time

all_time = {}
all_time = merge(merge(times[1],times[2]),times[3])
print(all_time)

# 获取邻近时间值，如果相邻位置距离相同，则选择左边
# all_time：所有时间列表；time:某设备时间列表；volt:某设备电压列表；i:all_time的索引；index:time的索引
def getNeighbour(all_time, time, volt, i, index):
    if index == 0:
        return volt[0]
    elif (all_time[i]-time[index - 1]) <= (time[index]-all_time[i]):
        return volt[i - 1]
    else:
        return volt[i]

# 对所在时间内不存在的电压进行插值处理，参数说明和上面一样
def insertValue(all_time, times, device_no):
    index = 0
    for i in range(len(all_time)):
        if index == len(times[device_no]) and i == len(all_time):
            break
        elif index == len(times[device_no]):
            volts[device_no].insert(i,volts[device_no][i-1])
        elif times[device_no][index] == all_time[i]:
            index = index+1
        else:
            volts[device_no].insert(i, getNeighbour(all_time, times[device_no], volts[device_no], i, index))

for device_no in range(1, ndevices+1):
    insertValue(all_time, times, device_no)
    print(volts[device_no])

