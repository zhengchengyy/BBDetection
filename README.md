## 2018/10/9

### 任务更新

- 查找在Linux系统上打开WiFi热点的方法

- 将一台Linux主机或者其中一台Beaglebone设置为NTP服务器

- 分析将TCP传输方式改为UDP的可行性，了解服务器上同时刻TCP连接数上限

- *同步精确到μs级（需要让老汪买服务器）

- wifi连接个数有没有上限，会不会影响延迟

## 2018/10/11

### 任务更新

- 放弃使用NTP协议，改为使用PTP协议。可行性参考<http://linuxptp.sourceforge.net/>

- 掌握PTP使用方法：

  a参考TI的指南：[ICSS PTP 1588 Developer Guide](http://processors.wiki.ti.com/index.php?title=ICSS_PTP_1588_Developer_Guide&oldid=229581) 

  b参考sourceforge的官方网站：[linuxptp](https://sourceforge.net/projects/linuxptp/)

  c参考ptpd的github项目：[ptpd](https://github.com/ptpd/ptpd)

- 搭建用于采集以及处理检波器数据的平台，建立数据库