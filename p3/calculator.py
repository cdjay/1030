import sys
import csv

class Args:

    def __init__(self):
        self.args=sys.argv[1:]

        try:
            self.rate=self.args[self.args.index('-c')+1]
            print("-c path:",self.rate,"pass!")
        except:
            print("error:No '-c' path for Config")

        try:
            self.user_data=self.args[self.args.index('-d')+1]
            print("-d path:",self.user_data,"pass!")
        except:
            print("error:No '-d' path for User")

        try:
            self.out_file=self.args[self.args.index('-o')+1]
            print("-o path:",self.out_file,"pass!")
        except:
            print("error:No '-o' path for User")


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
        except ss:
            print("Error:{} hava a some problem! Please check it!".format(path.rate))
        finally:
            return config

    def get(self,name):
        return self.config[name]


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

class IncomeTaxCalculator:

    def calc_for_all_userdata(self):
        #count=int(len(users.userdata))
        pass   
 
    def export(self,default='csv'):
        result=self.calc_for_all_userdata()
        print("output:",result)
        #with open(path.out_file) as f:
        #    writer = csv.writer(f)
        #    writer.writerows(result)


if __name__ == "__main__":
    path=Args()
    cfg=Config()
    users=UserData()
    gongzi=IncomeTaxCalculator()
    print(cfg.config)
    print(users.userdata)
    gongzi.export()
