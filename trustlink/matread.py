import pandas as pd
import numpy as np
def read_excel(filename):
    data = pd.read_excel(filename)
    data2 = data.drop(['index'], axis=1)
    adjarr = np.array(data2)
    return adjarr
