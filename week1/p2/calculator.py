#!/usr/bin/env python3
import sys

cashlist=sys.argv[1:]

for staff in cashlist:
    wages=staff.split(":")
    try:
        wages[1] = int(wages[1])
    except:
        print("Parameter Error")
        continue
    sstax= wages[1] * 0.165

    taxcash=wages[1]-3500-sstax

    if taxcash<=0:print("{}:{:.2f}".format(wages[0],wages[1]-sstax))
    elif taxcash <1500:print("{}:{:.2f}".format(wages[0], wages[1]-sstax-taxcash*0.03-0))
    elif taxcash >=1500 and taxcash <4500:print("{}:{:.2f}".format(wages[0], wages[1] - (sstax+taxcash * 0.10- 105)))
    elif taxcash >= 4500 and taxcash < 9000:print("{}:{:.2f}".format(wages[0], wages[1] - (sstax+taxcash * 0.20- 555)))
    elif taxcash >= 9000 and taxcash < 35000:print("{}:{:.2f}".format(wages[0], wages[1]-(sstax+taxcash * 0.25 - 1005)))
    elif taxcash >= 35000 and taxcash < 55000:print("{}:{:.2f}".format(wages[0], wages[1] - (sstax+taxcash * 0.30 - 2755)))
    elif taxcash >= 55000 and taxcash < 80000:print("{}:{:.2f}".format(wages[0], wages[1] - (sstax+taxcash * 0.35 - 5505)))
    elif taxcash >= 80000:print("{}:{:.2f}".format(wages[0], wages[1] -(sstax+taxcash * 0.45 - 13505)))
