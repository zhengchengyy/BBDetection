from abc import ABC, abstractmethod
from queue import Queue

class ProcessModule(ABC):
    """抽象类，表示处理数据的模块。
    每一个继承ProcessModule的类都包含一个存储数据的队列queue。
    继承该类需要重写processFullQueue方法。
    """

    def __init__(self, maxsize, leapsize):
        """构造方法中，参数中的maxsize表示队列的最大长度，
        leapsize表示在两次处理队列的间隔内，队列中新增元素的个数
        """
        if isinstance(maxsize, int) and isinstance(leapsize, int):
            if leapsize < 1 or maxsize < 1 or leapsize > maxsize - 1:
                raise ModuleProcessException("Illegal leapsize or maxsize.")
        else:
            raise ModuleProcessException("Maxsize and leapsize both should be integers.")
        self.maxsize = maxsize
        self.leapsize = leapsize
        self.queue = Queue(maxsize=maxsize)
        super(ProcessModule, self).__init__()

    @abstractmethod
    def processFullQueue(self):
        """处理满队列中的所有元素，通常为统计值。需要返回值。"""
        pass

    def process(self, value):
        """接收一个值，将其添加到队列中，如果队列已满，则移除队列中的leapsize个元素再添加。
        如果添加后队列为满队列，则执行processFullQueue方法。
        """
        if not self.queue.full():
            self.queue.put(value)
        else:
            for i in range(0, self.leapsize):
                self.queue.get()
            self.queue.put(value)
        if self.queue.full():
            return self.processFullQueue()


class FeatureExtractor:
    """提取特征值的类，该类需要配合ProcessModule使用。
    FeatureExtractor中有一个用于存储ProcessModule的列表，使用register函数可以向列表中添加ProcessModule。
    当FeatureExtractor接受到一个数据的时候，会让该列表中的所有PrcessModule接收这个数据并分别处理。
    """

    def __init__(self):
        self.modules = []

    def register(self, processModule):
        """添加一个ProcessModule"""
        self.modules.append(processModule)

    def process(self, value):
        """接收一个value值，让self.modules中的每一个ProcessModule处理该值，
        并调用func函数处理每一个ProcessModule的返回值。
        这里的func默认为简单的打印函数，可以设置为通过socket发送到其他设备的函数。"""
        result = {}
        for module in self.modules:
            # feature_name = module.FEATURE_NAME
            output = module.process(value)
            if (output != None):
                # result.append(module.FEATURE_NAME,output)
                result[module.FEATURE_NAME]=output
        return result


class SumModule(ProcessModule):
    """一个简单的ProcessModule，功能是对满队列中的所有数据求和。返回和。"""

    FEATURE_NAME = "SumModule"

    def processFullQueue(self):
        sum = 0
        for value in self.queue.queue:
            sum = sum + value
        return sum


class ModuleProcessException(Exception):
    pass