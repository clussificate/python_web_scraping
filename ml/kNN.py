import numpy as np
from numpy import *


def cosdist(vector1, vector2):
    return dot(vector1, vector2)/linalg.norm(vector1)*linalg.norm(vector2)

# 测试集：testdata， 训练集：trainset, 类别标签：listClasses, 近邻数：k
def classify(testdata, trainset, listClasses, k):
    datasetSize = trainset.shape[0]
    distances = array(zeros([datasetSize]))
    for index in range(datasetSize):
        distances[index] = cosdist(testdata, trainset[index])
    sortedDistIndicies = argsort(-distances)  # 降序排列，获取索引
    classCount={}
    for i in range(k):
        voteIlabel = listClasses[sortedDistIndicies[i]]
        # 为字典classcount赋值，相同的key,其值加1
        classCount[voteIlabel] = classCount.get(voteIlabel, 0)+1

    #对字典按照value值大小重新排序

    sortedClassCount = sorted(classCount.items(), key=lambda item: item[1], reverse=True)
    return sortedClassCount[0][0]
