'''
修改原有的feature_extractor文件，将按次数处理获得的数据改为按时间段处理
新增以及改变的代码均使用两行------标识
使用观察者模式实现特征提取，特征提取器(Subject)依赖于多个特征提取模块(Observer)，特征提取器注册了多个特征提取模块，
当特征提取器状态改变(获取到新数据)，通知所有特征模块更新状态(计算新的特征值)。
'''

from abc import ABC, abstractmethod
from queue import Queue

class ProcessModule(ABC):
    """Observer的抽象类，表示处理数据的模块。
    每一个继承ProcessModule的类都包含一个存储数据的队列queue。
    继承该类需要重写processFullQueue方法。
    """

#改变为时间存储后，构造函数改变为如下
#------
    def __init__(self, interval = 1, rate = 0.5, size = 0):
        """构造方法中，参数中的interval表示每次分析的时间跨度，
        rate表示间隔多长时间进行一次分析
        上述参数的单位均为秒
        """
        if (isinstance(interval, float) or isinstance(interval, int)) and (isinstance(rate, float) or isinstance(rate, int)):
            if interval <= 0 or rate <=0 or rate > interval:
                raise ModuleProcessException("Illegal rate or interval.")
        else:
            raise ModuleProcessException("Interval and rate both should be float or int.")
        self.interval = interval
        self.rate = rate
        self.size = size
        # 考虑采集数据频率可能变化,且分析时间会变化，因此不设定队列最大长度
        self.queue = Queue(maxsize = 0)
        super(ProcessModule, self).__init__()
#------

    @abstractmethod
    def processFullQueue(self):
        """处理满队列中的所有元素，通常为统计值。需要返回值。"""
        pass

    def process(self, value):
        """Observer的update()，接收一个值，将其添加到队列中，如果队列中头尾的数据达到了interval定义的时间差，则进行处理，
        并在处理后移除rate定义的时间差的。
        """
        self.queue.put(value)
        self.size +=1
        if value['time'] - self.queue.queue[0]['time'] > self.interval:
            result = self.processFullQueue()
            t = value['time']
            t_0 = self.queue.queue[0]['time']
            t_interval = self.interval - self.rate
            while value['time'] - self.queue.queue[0]['time'] > self.interval - self.rate:
                self.queue.get()
                self.size -= 1
            return result


class FeatureExtractor:
    """Subject提取特征值的类，该类需要配合ProcessModule使用。
    FeatureExtractor中有一个用于存储ProcessModule的列表，使用register函数可以向列表中添加ProcessModule。
    当FeatureExtractor接受到一个数据的时候，会让该列表中的所有PrcessModule接收这个数据并分别处理。
    """

    def __init__(self):
        self.modules = []

    def register(self, processModule):
        """添加一个ProcessModule"""
        self.modules.append(processModule)

    def process(self, value):
        """Subject的notify(),接收一个value值，让self.modules中的每一个ProcessModule处理该值"""
        result = {}
        for module in self.modules:
            output = module.process(value)
            if (output != None):
                result[module.FEATURE_NAME] = output
        return result

    def clear(self):
        """清理所有的ProcessModule"""
        for module in self.modules:
            module.clear()

class ModuleProcessException(Exception):
    pass