# ! /usr/bin/env python3
# ! -*- coding:utf8 -*-

import sys
import csv
# from multiprocessing import Process, Queue

# 参数处理 (  tax:税率 user_data:用户薪资 out_file:输出 city:城市  )
class Args:

    # 初始化
    def __init__(self):
        # 获取命令行列表
        self.args = sys.argv[1:]
        # 处理参数
        self._get_parameter()

    # 处理参数函数
    def _get_parameter(self):
        # 参数字典
        arglist = {
            "-C": "所在城市名称",
            "-c": "税率配置文件",
            "-d": "员工薪资原始文件",
            "-o": "生成工资条文件",
            "-h": "Usage: calculator.py -C cityname -c configfile -d userdata -o resultdata",
            "--help": "Usage: calculator.py -C cityname -c configfile -d userdata -o resultdata"
        }

        if "-h" in self.args or "--help" in self.args:
            print(arglist['-h'])
            return
        else:
            try:
                self.tax = self.args[self.args.index('-c') + 1]
                self.data = self.args[self.args.index('-d') + 1]
                self.result = self.args[self.args.index('-o') + 1]
                # self.city = self.args[self.args.index('-C') + 1]
            except:
                print("Error: 没有输入足够的参数 请输入 [-h] 或者 [--help] 查看使用帮助 ")


# 获取税率配置 (  config 字典  )
class Tax:

    def __init__(self, path):
        # 读取配置
        self.config = self._read_config(path)

    def _read_config(self, path):
        config = {}
        try:
            with open(path, 'r') as f:
                for x in f:
                    dict = x.split("=")
                    config[dict[0].strip()] = float(dict[1].strip())
        except:
            print("Error:{} hava a some problem! Please check it!".format(path))
        finally:
            return config

    def get(self, name):
        return self.config[name]


# 获取用户原始数据 (  data 字典  )
class Staff:

    def __init__(self, path):
        self.data = self._read_staffdata(path)

    def _read_staffdata(self, path):
        data = {}
        try:
            with open(path, 'r') as f:
                for x in f:
                    dict = x.split(",")
                    data[dict[0].strip()] = float(dict[1].strip())
        except:
            print("Error:{} hava a some problem! Please check it!".format(path))
        finally:
            return data

# 计算工资
class IncomeTaxCalculator:

    # 初始化
    def __init__(self):
        self.ladder =[
            [80000, 0.45, 13505],
            [55000, 0.35, 5505],
            [35000, 0.3, 2755],
            [9000, 0.25, 1005],
            [4500, 0.2, 555],
            [1500, 0.1, 105],
            [0, 0.03, 0]
        ]
    # 社保金额
    def YNSuode(self, pay):

        taxpay=pay
        # 社保计算基数
        if pay >= tax.get('JiShuH'):taxpay=tax.get('JiShuH')
        if pay <= tax.get('JiShuL'): taxpay = tax.get('JiShuL')

        # 社保费率
        soctax=tax.get('YangLao')
        soctax+= tax.get('YiLiao')
        soctax += tax.get('ShiYe')
        soctax += tax.get('GongShang')
        soctax += tax.get('ShengYu')
        soctax += tax.get('GongJiJin')

        return taxpay*soctax

    # 个税金额
    def GS(self, pay,sbje):
        # 计算应征额度
        shui=pay-sbje-3500

        if shui <=0:shui=0
        for num in range(len(self.ladder)):
            dangci,shuilv,susuan=self.ladder[num][0],self.ladder[num][1],self.ladder[num][2]
            if shui >= dangci:
                return shui*shuilv-susuan

    # 计算并输出
    def export(self):
        with open(path.result,'w',newline='') as file:
            csv_writer=csv.writer(file)
            for name, pay in staff.data.items():
                # 社保金额
                sbje=self.YNSuode(pay)
                # 个税金额 传入工资,社保)
                gsje=self.GS(pay,sbje)
                out="{},{:.2f},{:.2f},{:.2f},{:.2f}".format(name,pay,sbje,gsje,pay-sbje-gsje).split(',')
                csv_writer.writerow(out)



if __name__ == "__main__":
    # 开进程
    # queue = Queue(maxsize=3)

    # 数据处理
    try:
        # 处理参数
        path = Args()
        # 读取税率文件
        tax = Tax(path.tax)
        # 读取员工数据
        staff = Staff(path.data)
    except:
        print("读取文件发生未知错误,请检查数据格式是否正确!")

    gongzi=IncomeTaxCalculator()
    gongzi.export()
