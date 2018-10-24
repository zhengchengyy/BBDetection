## 2018/10/9

### 任务更新

- 查找在Linux系统上打开WiFi热点的方法

- 将一台Linux主机或者其中一台Beaglebone设置为NTP服务器

- 分析将TCP传输方式改为UDP的可行性，了解服务器上同时刻TCP连接数上限

- *同步精确到μs级

- wifi连接个数有没有上限，会不会影响延迟

## 2018/10/11

### 任务更新

- 放弃使用NTP协议，改为使用PTP协议。可行性参考<http://linuxptp.sourceforge.net/>

- 掌握PTP使用方法：

  a参考TI的指南：[ICSS PTP 1588 Developer Guide](http://processors.wiki.ti.com/index.php?title=ICSS_PTP_1588_Developer_Guide&oldid=229581) 

  b参考sourceforge的官方网站：[linuxptp](https://sourceforge.net/projects/linuxptp/)

  c参考ptpd的github项目：[ptpd](https://github.com/ptpd/ptpd)

- 搭建用于采集以及处理检波器数据的平台，建立数据库

## 2018/10/24

测试得到一组数据，因为同步存在问题，只有一台设备的时间是基本正确的，所以只有得到了一个beaglebone的数据。根据这些数据画图：

![lay_down](https://images.gitee.com/uploads/images/2018/1024/101411_d9531a88_1602036.png "Figure_1.png")
![sit_up](https://images.gitee.com/uploads/images/2018/1024/101431_8a1c16dc_1602036.png "situp.png")
![vacant](https://images.gitee.com/uploads/images/2018/1024/101448_9d6e3416_1602036.png "vacant.png")
![walkby](https://images.gitee.com/uploads/images/2018/1024/101458_4b23c0fc_1602036.png "walkby.png")
![sleep](https://images.gitee.com/uploads/images/2018/1024/101910_791690f5_1602036.png "sleep.png")