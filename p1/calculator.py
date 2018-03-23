#!/usr/bin/env python3
import sys

try:
    cash=int(sys.argv[1])
    cash=cash-0-3500
    if cash <1500:print("{:.2f}".format(cash*0.03-0))
    elif cash >=1500 and cash < 4500:print("{:.2f}".format(cash*0.1-105))
    elif cash >=4500 and cash < 9000:print("{:.2f}".format(cash*0.2-555))
    elif cash >=9000 and cash < 35000:print("{:.2f}".format(cash*0.25-1005))
    elif cash >=35000 and cash < 55000:print("{:.2f}".format(cash*0.30-2755))
    elif cash >=55000 and cash < 80000:print("{:.2f}".format(cash*0.35-5505))
    elif cash >=80000:print("{:.2f}".format(cash*0.45-13505))
except:
    print("Parameter Error")
