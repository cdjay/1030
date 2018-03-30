import sys
import csv

# 参数处理
class Args:

    # 初始化
    def __init__(self):
        self.args=sys.argv[1:]

        try:
            self.rate=self.args[self.args.index('-c')+1]
            # print("-c path:",self.rate,"pass!")
        except:
            print("error:No '-c' path for Config")

        try:
            self.user_data=self.args[self.args.index('-d')+1]
            # print("-d path:",self.user_data,"pass!")
        except:
            print("error:No '-d' path for User")

        try:
            self.out_file=self.args[self.args.index('-o')+1]
            # print("-o path:",self.out_file,"pass!")
        except:
            print("error:No '-o' path for User")

# 获取税率设置
class Config:

    def __init__(self):
        self.config = self._read_config()

    def _read_config(self):
        config={}
        try:
            with open(path.rate) as f:
                for x in f:
                    dict=x.split("=")
                    config[dict[0].strip()]=float(dict[1].strip())
        except :
            print("Error:{} hava a some problem! Please check it!".format(path.rate))
        finally:
            return config

    def get(self,name):
        return self.config[name]

# 获取用户原始数据
class UserData:

    def __init__(self):
        self.userdata=self._read_user_data()

    def _read_user_data(self):
        userdata=[]
        try:
            with open(path.user_data) as f:
                for x in f:
                    x=x.strip()
                    userdata+=x.split(",")
        except:
            print("Error:{} hava a some problem! Please check it!".format(path.user_data))
        
        try:
           for x in range(len(userdata)):
               userdata[x]=float(userdata[x])
        except:
           print("error:userdata is not int")
        return userdata

#计算工资
class IncomeTaxCalculator:

    def calc_for_all_userdata(self):
        c=users.userdata
        social_tax=cfg.get('YangLao')+cfg.get('YiLiao')+cfg.get('ShiYe')+cfg.get('GongShang')+cfg.get('ShengYu')+cfg.get('GongJiJin')
        level={
            1:(0.03,0),
            2:(0.10,105),
            3:(0.20,555),
            4:(0.25,1005),
            5:(0.30,2755),
            6:(0.35,5505),
            7:(0.45,13505)
        }
        self.out=[]
        for x in range(int(len(c)/2)):
            self.out.append(str(int(c[x*2])))
            self.out.append("%.2f"%c[x*2+1])
            if c[x*2+1] <cfg.get('JiShuL'):stax=cfg.get('JiShuL')*social_tax
            elif c[x*2+1] >cfg.get('JiShuH'):stax=cfg.get('JiShuH')*social_tax
            else:stax=c[x*2+1] *social_tax
            self.out.append("%.2f"%stax)
            ptax=c[x*2+1] -stax-3500
            if ptax<0:ptax=0
            if ptax > 80000:level_count=7
            elif ptax > 55000: level_count = 6
            elif ptax > 35000: level_count = 5
            elif ptax > 9000: level_count = 4
            elif ptax > 4500: level_count = 3
            elif ptax > 1500: level_count = 2
            else:level_count = 1
            ptax=ptax*level[level_count][0]-level[level_count][1]
            self.out.append("%.2f"%ptax)
            self.out.append("%.2f"%(c[x*2+1]-stax-ptax))
        return self.out

    def export(self):
        self.result=self.calc_for_all_userdata()

        out=[]
        for rows in range(int(len(self.result)/5)):
            out.append(self.result[rows*5:rows*5+5])

        with open(path.out_file,'w',newline="") as f:
            writer=csv.writer(f)
            writer.writerows(out)


if __name__ == "__main__":
    path=Args()
    cfg=Config()
    users=UserData()
    gongzi=IncomeTaxCalculator()
    gongzi.export()

