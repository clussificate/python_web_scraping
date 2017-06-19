from numpy import *
import matplotlib.pyplot as plt

def loadDataset(filename):
    x = []; y = []
    fr = open(filename)
    for line in fr.readlines():
        curline = line.strip().split('\t')
        x.append(float(curline[0])); y.append(float(curline[1]))
    return x,y

def plotscatter(xmat, ymat, a, b):
    fig = plt.figure()
    ax = fig.add_subplot(111)     # 绘制图形位置
    ax.scatter(xmat, ymat, c='blue', marker='o')
    xmat.sort()
    yhat = [a*float(xi)+b for xi in xmat]
    plt.plot(xmat,yhat,'r')
    plt.show()
    return yhat


xmat, ymat= loadDataset("regdataset.txt")
meanx = mean(xmat)
meany = mean(ymat)
dx = xmat-meanx
dy=ymat-meany

sumxy = vdot(dx,dy)
sqx = sum(power(dx,2))

a = sumxy/sqx
b = meany-a*meanx
print(a, b)
plotscatter(xmat,ymat,a,b)

