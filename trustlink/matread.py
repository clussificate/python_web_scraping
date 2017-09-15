import pandas as pd
import numpy as np
import os
def read_data(filename):
    pwd = os.getcwd()
    os.chdir(os.path.dirname(filename))
    data = pd.read_csv(os.path.basename(filename),index_col=0)
    os.chdir(pwd)
    adjarr = np.array(data)
    return adjarr

if __name__ == "__main__":
    adj = read_data(r'D:\资料\信任网络\trustmat.csv')
    print(adj)

