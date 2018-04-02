# !usr/bin/env python3

import sys
import csv
import queue
from multiprocessing import Process, Queue


# 甩出错误
class ArgError(Exception):
    pass


# 参数处理
class Args:

    # 初始化
    def __init__(self, args):
        # 获取命令行参数
        self.args = args

    # 处理
    def __parse_arg(self, arg):
        try:
            value = self.args[self.args.index(arg) + 1]
        except(ValueError, IndexError):
            value = None
        return value

    # 获取路径
    def get_arg(self, arg):
        value = self.__parse_arg(arg)

        if value is None:
            raise ArgError('Not found arg {}'.format(arg))
        return value


# 读取社保配置
class SheBaoConfig:

    def __init__(self, file):

        self.jishu_low, self.jishu_high, self.rate = self.__parse_config(file)

    def __parse_config(self, file):

        rate = 0
        jishu_low = 0
        jishu_high = 0

        with open(file) as f:
            for line in f:
                key, value = line.split('=')
                key = key.strip()
                try:
                    value = float(value.strip())
                except ValueError:
                    continue
                if key == 'JiShuL':
                    jishu_low = value
                elif key == 'JiShuH':
                    jishu_high = value
                else:
                    rate += value
        return jishu_low, jishu_high, rate


class StaffData(Process):

    def __init__(self, file, output_queue):

        self.file = file
        self.output_q = output_queue
        super().__init__()

    @property
    def __parse_data(self):
        # 一次一行
        for line in open(self.file):
            staff_id, gongzi = line.split(',')
            yield (int(staff_id), int(gongzi))

    def run(self):

        for item in self.__parse_data:
            self.output_q.put(item)


class Calculator(Process):

    #  起征点
    tax_start = 3500

    # 速查表(应纳税额,税率,速算扣除数)
    tax_table = [
        (80000, 0.45, 13505),
        (55000, 0.35, 5505),
        (35000, 0.3, 2755),
        (9000, 0.25, 1005),
        (4500, 0.2, 555),
        (1500, 0.1, 105),
        (0, 0.03, 0),
    ]

    def __init__(self, config, input_queue, out_queue):

        self.config = config
        self.input_q = input_queue
        self.output_q = out_queue

        # 手动调用__init__
        super().__init__()

    def calculate(self, data_item):

        employee_id, gongzi = data_item

        if gongzi < self.config.jishu_low:
            shebao = self.config.jishu_low * self.config.total_rate
        elif gongzi > self.config.jishu_high:
            shebao = self.config.jishu_high * self.config.total_rate
        else:
            shebao = gongzi * self.config.rate

        # 参与计算
        left_gongzi = gongzi - shebao

        # 应纳税所得额
        tax_gongzi = left_gongzi - self.tax_start

        # 判断是否有个税
        if tax_gongzi < 0:tax = 0
        else:
            for item in self.tax_table:
                if tax_gongzi > item[0]:
                    tax = tax_gongzi * item[1] - item[2]
                    break

        # 最终工资
        last_gongzi = left_gongzi - tax

        return str(employee_id), str(gongzi),'{:.2f}'.format(shebao),'{:.2f}'.format(tax),'{:.2f}'.format(last_gongzi)

    def run(self):
        # 循环获取数据,指定超时时间,如果超时则推出
        while True:
            try:item = self.input_q.get(timeout=1)
            except queue.Empty:return
            # 将结果放到队列中
            result = self.calculate(item)
            self.output_q.put(result)

class Exporter(Process):

    def __init__(self, file, input_queue):

        self.file = open(file, 'w')
        self.input_q = input_queue
        # 手动调用__init__
        super().__init__()

    def export(self, item):
        line = ','.join(item) + '\n'
        self.file.write(line)

    def close(self):
        self.file.close()

    def run(self):
        while True:
            try:
                # 循环获取数据,指定超时时间,如果超时则推出
                item = self.input_q.get(timeout=1)
            except queue.Empty:
                self.close()
                return
            self.export(item)


# 执行
if __name__ == "__main__":
    # 读取参数
    path = Args(sys.argv[1:])
    # 读取社保
    config = SheBaoConfig(path.get_arg('-c'))

    queue1 = Queue()
    queue2 = Queue()

    # 读取员工
    staff_data = StaffData(path.get_arg('-d'), queue1)
    # 计算工资
    calculator = Calculator(config, queue1, queue2)
    # 导出文件
    exporter = Exporter(path.get_arg('-o'), queue2)

    # 启动
    staff_data.start()
    calculator.start()
    exporter.start()

    staff_data.join()
    calculator.join()
    exporter.join()
