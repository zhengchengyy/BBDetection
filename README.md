## **基于软件定义智能的睡眠监测系统（Python）**

项目简介：通过传感器采集数据，再通过BeagleBone开发板提取数据特征，根据分布的不同节点的特征来推理出人的睡眠状态，实现了实时画图、数据存储、特征提取、推理机推理功能。

实验结果展示如下，更多结果可以在data目录下找到：

<https://github.com/zhengchengyy/BBDetection/blob/master/data/424%E6%95%B0%E6%8D%AE/424turn_over.png>

项目采用基于软件定义智能的技术对老年人进行睡眠监测，把智能环境的数据层和控制层相分离，根据不同老年人的活动状况来自定义相关规则，控制层通过推理机根据规则推理的结果采取相应措施；通过分布式推理的方式充分利用了各个传感器结点的计算资源，减少了由于网络传输大量原始数据而产生的时延；并给出了软件定义智能的通用模型（数据层、特征层、推理层、控制层），可以在大部分智能环境设备中复用。我们的方法理论上可以解决老年人睡眠的监测，为老年人健康隐患和紧急危险提供安全保障。下面是该项目技术上的一些简单介绍：

### 1、时间同步怎么实现的，NTP协议是什么？

NTP：基于UDP，用于网络时间同步的协议，使网络中的计算机时钟同步到UTC，再配合各个时区的偏移调整就能实现精准同步对时功能。

- 安装＃sudo apt-get install ntpdate
- 手动同步系统时间# sudo ntpdate cn.pool.ntp.org  或者sudu ntpdate time.windows.com
- 其他slave机器就他 ntpdate 192.168.1.222(主机ip或者域名)

改进：每次都需要重新配置时间，可以写成脚本的形式随系统启动进行配置时间。

### 2、设计队列来实现原始数据的特征提取

思想：参考网络传输模型，设计一个队列，队列包含容量和步长(因为震动数据是实时产生的，要统计不同时间的特征，队列需要不停添加和丢弃数据，丢弃数据的多少其实就是步长，类似于一个固定大小滑动窗口不断往前移)，根据时间计算队列里数据的特征，比如平方差、平均值、极值、阈值次数等，表示在不同时间的特征。

如图所示，参照观察者模式，定义了一个处理模块抽象类，该类包含一个队列、一个处理满队列的抽象方法、一个实例方法用于队列添加和删除元素，满时调用处理满队列方法。还定义了一个特征提取类，该类包含一个模块列表，一个注册的实例方法用于添加特征提取模块，一个处理的实例方法用于处理模块列表中的特征模块，处理完的结果存入字典。另外还定义了几个继承处理模块的特征模块类用于提取特征，这些类实现了处理模块类的抽象方法。

### 3、多线程技术来实现数据的实时画图

当客户端给服务器发送数据时，客户端需要接收数据存入MongoDB数据库，并且需要支持实时画图。但是画图时卡住了，只显示了画布，没有图像，后台数据正常发送。主要问题应该是画图占用主线程太多资源，利用多线程解决，一个线程用于接收数据存入MongoDB数据库，另一个线程以阻塞的方式把接收的数据进行画图。

### 4、什么时软件定义智能，怎么实现？设计系统的模型结构

软件定义智能：简单来说就是对于不同设备和不同年龄人的睡眠监测，不需要改变原始代码，只需要改变规则，即可快速的实现不同的模式识别规则，完善传统的对于不同人群需要重新建立模式识别代码的问题。

怎么实现：根据半监督式学习统计出相关规则，再利用基于规则的推理机进行推理。如果设备变更或者监测者变更则重新产生规则进行推理。

模型结构：数据层、特征层、推理层、控制层。不同层的功能不同， 通过分层明确不同层的任务，使系统分工明确，通过接口不同层之间进行数据交互。比如数据层通过采集震动数据，特征层获取数据层的数据进行特征提取，推理层根据特征层的数据进行推理，把推理的结果交给控制层，控制层获取数据后进行响应控制。

### 5、使用 UDP 协议来实现数据传输

参考redis主从模式。选取一个板子作为主设备，其它作为从设备。从设备把提取的特征或者推理的结果按照UDP协议发送给主设备，主设备把获取到的数据进行推理，得到最终结论，并做出响应控制。如果主设备瘫痪，则根据投票的方式从其它从设备中选出新的主设备（待完成）。

### 6、使用插值法来实现数据同步

为什么需要时间同步，因为不同节点采集的数据不在同一时间点上，如果画图出来它们的数据之间没有可比性。可以利用插值法，如果该节点在某个时间点不存在数据，则把就近时间的数据插入进去。

### 7、使用 MongoDB来存储和读取数据

采集的数据为时间及其对应时间点的电压值，设计为JSON格式方便存储和查询，而MongoDB非常适合存储JSON格式数据；并且任何属性都可索引便于查询；数据操作会先写入内存，然后再会持久化到硬盘中去，性能极高；以 BSON 结构（二进制）进行存储，适合大数据存储。

注意：2、6和7部分的代码链接：<https://github.com/zhengchengyy/BBDataProcessing>