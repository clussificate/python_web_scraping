from numpy import *
import matplotlib.pyplot as plt
def loadDataset(filename):
    datamat = []; labelmat = []
    with open(filename) as fr:
        for line in fr.readlines():
            lineArr = line.strip().split()
            datamat.append([1.0, float(lineArr[0]), float(lineArr[1])])
            labelmat.append(int(lineArr[2]))
    return datamat, labelmat

def sigmoid(inX):
    return 1.0/(1+exp(-inX))


# 梯度上升优化
def gradAscent(datamatIn, classLabels):
    datamatrix = mat(datamatIn)
    labelMat = mat(classLabels).T
    m, n = shape(datamatrix)
    alpha = 0.001
    maxcycles = 500
    weights = ones((n,1))
    for i in range(maxcycles):
        h = sigmoid(datamatrix*weights)
        error = (labelMat - h)              # 大样本时，可将样本分割，用多个小批量样本进行迭代
        weights = weights + alpha * datamatrix.T * error # 具体原理参见《机器学习》p.60
    return weights

# 随机梯度上升
def stocGradAscent(datamatrix,classlabels,numIter = 150):
    datamatrix = mat(datamatrix)
    m,n = shape(datamatrix)
    weights = ones((n, 1))
    for j in range(numIter):
        dataIndex = list(range(m))
        for i in range(m):
            alpha = 4/(1.0+j+i)+0.0001
            randIndex = int(random.uniform(0,len(dataIndex)))
            h = sigmoid(sum(datamatrix[randIndex]*weights))
            error = classlabels[randIndex]-h
            weights = weights +alpha*error*datamatrix[randIndex].T
            del(dataIndex[randIndex])
    return weights

# 可视化
def plotBestFit(wei,filename):
    weights = array(wei)
    datamat, labelmat = loadDataset(filename)
    dataArr = array(datamat)
    n = shape(dataArr)[0]
    xcord1=[]; ycord1=[]
    xcord2=[]; ycord2=[]
    for i in range(n):
        if int(labelmat[i])==1:
            xcord1.append(dataArr[i,1]);ycord1.append(dataArr[i,2])
        else:
            xcord2.append(dataArr[i,1]);ycord2.append(dataArr[i,2])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(xcord1,ycord1,s=30,c='red',marker='s')
    ax.scatter(xcord2,ycord2,s=30,c='green',marker='o')
    x=arange(-3.0,3.0,0.1)
    y=(-weights[0]-weights[1]*x)/weights[2]
    ax.plot(x,y)
    plt.xlabel("x1");plt.ylabel('x2')
    plt.show()



filename = "D:/资料/机器学习实战/machinelearninginaction/Ch05/testSet.txt"
dataArr, labelmat = loadDataset(filename)
weights = gradAscent(dataArr, labelmat)
weights2 = stocGradAscent(dataArr, labelmat)
print(weights,weights2)
plotBestFit(weights, filename)
