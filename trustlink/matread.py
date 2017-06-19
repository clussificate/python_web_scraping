import xlrd
import numpy as np

data = xlrd.open_workbook('data1.xlsx')
table = data.sheets()[0]
nrows = table.nrows
ncols = table.ncols
myarr = np.zeros([19,19])
for i in range(nrows - 1):
    myarr[i] = table.row_values(i + 1)[1:]

