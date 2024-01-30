import csv
import pandas as pd
import numpy as np




def kayit(aci,enkoder,csvisim): 

    aciList = []
    enkoderList = []
    allList = []
    with open(f"{csvisim}.csv",newline="") as file:

        r = csv.reader(file)

        for row in r:
            allList.append(row)
        
        file.close()

    aciList = allList[0]
    enkoderList = allList[1]

    aciList.append(aci)
    enkoderList.append(enkoder)
    """
    print(f"aci = {aciList}")
    print(f"enkoder = {enkoderList}")
    print(f"mesafe = {mesafeList}")"""

    with open(f"{csvisim}.csv","w",newline="") as file :
        
        w = csv.writer(file)
        w.writerow(aciList)
        w.writerow(enkoderList)

        file.close

#kayit("100","55","32")