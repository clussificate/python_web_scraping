from numpy import *
import matplotlib.pyplot as plt
#计算欧式距离

def eucDistance(vector1,vector2):
    return(sqrt(sum(power((vector1-vector2),2))))

#随机选取4个点作为初始质心
def initCentroids(dataSet, k):       #k表示要创建的聚类数
    numSamples, dim = dataSet.shape           #样本大小和维度
    centroids = zeros((k, dim))        #用零填充初始质心矩阵
    for i in range(k):
        index = int(random.uniform(0, numSamples))
        centroids[i, :] = dataSet[index, :]
    return(centroids)

# 聚类过程
def Kmeans(dataSet, k, centroids):
    numSamples = dataSet.shape[0]
    clusterAssment = zeros((numSamples, 2))   # 每个样本的类别构成的表 （类别，距离）
    clusterChanged = True

    while clusterChanged:
        clusterChanged = False
        for i in range(numSamples):
            minDist = 100000.0
            minIndex = 0

            #计算所有点与所有质心的距离
            for j in range(k):
                distance = eucDistance((centroids[j]), (dataSet[i]))
                if distance < minDist:
                    minDist = distance
                    minIndex = j
              # 更新聚类
            if clusterAssment[i, 0] != minIndex:
                 clusterChanged = True
                 clusterAssment[i, :] = minIndex, minDist

              #更新质心，注意此处所用的分类方法
        for j in range(k):
            # nonzero返回2维元祖，分别存放行,列指标。本例需返回行指标,返回行列指标则只能产生一个数
            pointIncluster = dataSet[nonzero(clusterAssment[:, 0] == j)[0]]
            centroids[j, :] = mean(pointIncluster, axis=0)    #axis=0是按列分别取平均值

    print("Congratulations:cluster complete!")
    return(centroids, clusterAssment)



def showcluster(dataSet, k, centroids, clusterAssment):
    numSamples, dim = dataSet.shape
    if dim != 2:
        print("Sorry! I can not draw because the dimension of your data is not 2!")
        return 1
    mark = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']
    if k > len(mark):
        print("Sorry! Exceed the quantity! please reduce the amount of classes")
    #画出所有的聚类数据，根据所处聚类中心的不同用不同的表示方法
    for i in range(numSamples):
        markIndex = int(clusterAssment[i, 0])
        plt.plot(dataSet[i, 0], dataSet[i, 1], mark[markIndex])
    #画出聚类中心
    mark = ['Dr', 'Db', 'Dg', 'Dk', '^b', '+b', 'sb', 'db', '<b', 'pb']
    for i in range(k):
        plt.plot(centroids[i, 0],centroids[i, 1], mark[i], markersize=12)

    plt.show()

print("step1: 加载数据")
dataSet = []
with open("newtestSet.txt") as f:
    for line in f:
        lineArr = line.strip().split(',')
        dataSet.append([float(lineArr[0]), float(lineArr[1])])
dataSet = array(dataSet)
print("step2: 请输出需要聚类的个数")
k = int(input())
print("初始化.....")
Initcentroids = initCentroids(dataSet, k)
# print(Initcentroids)
# print(eucDistance(Initcentroids[1],dataSet[1]))
print("step4: 开始聚类")
centroids, clusterAssment = Kmeans(dataSet, k, Initcentroids)
print("step5: 画出图形 ")
showcluster(dataSet, k, centroids, clusterAssment)













