from numpy import *
import  math
import copy
import pickle
class ID3DTree(object):
    def __init__(self):
        self.tree = {}   # 生成的树
        self.dataset = []   # 数据集
        self.labels = []   #标签集

    # 输入导入函数
    def loadDataSet(self, path, labels):
        recordlist = []
        fp = open(path, "rb")  # rb表示读写二进制数据
        content = fp.read()
        fp.close()
        rowlist = content.splitlines()  # 按行转换为一维表
        recordlist = [row.split('\t') for row in rowlist if row.strip()] # 重点
        self.dataset = recordlist
        self.labels = labels
    # 执行决策树函数
    def train(self):
        labels = copy.deepcopy(self.labels)  # 深拷贝  相当于新建一份文件 原文件改变不影响这个文件
        self.tree = self.buildTree(self.dataset, labels)

    # 构建决策树
    def buildTree(self, dataset, labels):
        cateList = [data[-1] for data in dataset]  # 抽取原数据集的决策标签列
        # 程序终止条件1：如果cateList 只有一种决策标签，停止划分，返回这个决策标签
        if cateList.count(cateList[0]) == len(cateList):
            return cateList[0]
        # 程序终止条件2： 如果数据集只有一个决策标签列，则返回这个决策标签列的最大值
        # 这种情况是划分到最后，群体还出现多种标签，则选择一个最大的标签输出
        if len(dataset[0]) == 1:
            return self.maxCate(cateList)

        # 算法核心
        bestFeat = self.getBestFeat(dataset)  # 返回数据集的最优特征轴
        bestFeatLabel = labels[bestFeat]
        #####！！！！！！！！
        tree = {bestFeatLabel: {}}   # 不断扩充的字典
        #####！！！！！！！
        del(labels[bestFeat])
        # 抽取最优特征轴的列向量
        uniqueVals = set([data[bestFeat] for data in dataset])  # 去重
        for value in uniqueVals:  # 决策树递归生长
            subLabels = labels[:]  # 将删除后的特征类别建立子类别集
            #按最优特征列和值分隔数据集
            splitDataset = self.splitDataset(dataset, bestFeat, value)
            subTree = self.buildTree(splitDataset, subLabels)
            tree[bestFeatLabel][value] = subTree
        return tree

    # 计算最优特征值
    def getBestFeat(self, dataset):
        # 计算特征向量维，其中最后一行用于类别标签，因此要减去
        numFeatures = len(dataset[0]) - 1
        baseEntropy = self.computeEntropy(dataset)
        bestInfoGain = 0.0  # 初始化最优的信息增益
        bestFeature = -1   # 初始化最优特征轴
        # 外循环：遍历数据集各列，计算最优特征轴
        #  i为数据集列索引， 取值在0~（numFeatures-1）
        for i in range(numFeatures):     # 抽取第i列的向量
            uniqueVals = set([data[i] for data in dataset])   # 去重：该列的唯一值集
            newEntropy = 0.0
            for value in uniqueVals:   # 内循环 按列和唯一值计算熵
                subDataset = self.splitDataset(dataset, i, value)
                prob = len(subDataset)/float(len(dataset))
                newEntropy += prob * self.computeEntropy(subDataset)
            infoGain = baseEntropy - newEntropy
            if (infoGain > bestInfoGain):
                bestInfoGain = infoGain
                bestFeature = i
        return bestFeature

    # 计算出现次数最多的类别标签
    def maxCate(self, cateList):
        items = dict([(cateList.count(i), i) for i in cateList])
        return items[max(items.keys())]

    # 计算香农值的函数】
    def computeEntropy(self,dataset):
        datalen = float(len(dataset))
        cateList = [data[-1] for data in dataset]   # 获取类别标签
        #得到类别为Key、出现次数Value的字典
        items = dict([(i, cateList.count(i)) for i in cateList])  # b = dict([(1, 3), (1, 3)]) = {1: 3}
        infoEntropy = 0.0
        for key in items:
            prob = float(items[key])/datalen
            infoEntropy -= prob * math.log(prob, 2)
        return infoEntropy


    # 划分数据集；分隔数据集；删除特征轴所在的数据列，返回剩余的数据集
    # axis:特征轴； value：特征轴的取值
    def splitDataset(self, dataset, axis, value):
        rtnList = []
        for featVec in dataset:
            if featVec[axis] == value:
                rFeatVec = featVec[ :axis]
                rFeatVec.extend(featVec[axis+1:])
                rtnList.append(rFeatVec)
        return rtnList



    # 决策树的分类器代码
    def predict(self, inputTree, featLabels, testVec):
        root = inputTree.keys()[0]
        secondDict = inputTree[root]   # value 子树结构或者分类标签
        featIndex = featLabels.index[root]    # 根节点在标签中的位置
        key = testVec[featIndex]    # 测试集数组取值
        valueOfFeat = secondDict[key]
        if isinstance(valueOfFeat, dict):
            classLabel = self.predict(valueOfFeat, featLabels,testVec) # 递归分类
        else:  classLabel = valueOfFeat
        return classLabel

    ###################################################################
    # C4.5：按信息增益划分最优节点的方法
    def getBestFeat2(self, dataset):
        num_feats = len(dataset[0][:-1])
        totality = len(dataset)
        BaseEntropy = self.computeEntropy(dataset)
        conditionEntropy = []     # 初始化条件熵
        splitInfo = []   # for c4.5, caculate gain ratio
        allFeatVList = []
        for f in range(num_feats):
            featList = [example[f] for example in dataset]    # 取列值
            [splitI, featureValueList] = self.computeSplitInfo(featList)
            allFeatVList.append(featureValueList)
            splitInfo.append(splitI)
            resultGain = 0.0
            for value in featureValueList:
                subset = self.splitDataset(dataset, f, value)
                appearNum = float(len(subset))
                subEntropy = self.computeEntropy(subset)
                resultGain += (appearNum/totality)*subEntropy
            conditionEntropy.append(resultGain)  # 总条件熵
        infoGainArr = BaseEntropy*ones(num_feats)-array(conditionEntropy)
        infoGainRatio = infoGainArr/array(splitInfo)    #   C4.5 信息增益算法
        bestFeatureIndex = argsort(-infoGainRatio)[0]    # 从大到小排列，找出最大值的索引
        return bestFeatureIndex, allFeatVList[bestFeatureIndex]


    # 计算划分信息（splitinfo）
    def computeSplitInfo(self, featureVList):
        numentries = len(featureVList)
        featureVauleSetList = list(set(featureVList))
        valueCounts = [featureVList.count(featVec) for featVec in featureVauleSetList]
        # caculate shannonEnt
        pList = [float(item)/numentries for item in valueCounts]
        lList = [item*math.log(item, 2) for item in pList]
        splitInfo = -sum(lList)
        return splitInfo, featureVauleSetList

    # C4.5 生成数函数
    def buildTree2(self, dataset, labels):
        cateList = [data[-1] for data in dataset]
        if cateList.count(cateList[0]) == len(cateList):
            return cateList[0]
        if len(dataset[0]) == 1:
            return self.maxCate(cateList)
        bestFeat, featValueList = self.getBestFeat(dataset)
        bestFeatLabel = labels[bestFeat]
        tree = {bestFeatLabel: {}}
        del (labels[bestFeat])
        for value in featValueList:
            subLabels = labels[:]
            splitDataset = self.splitDataset(dataset, bestFeat, value)
            subTree = self.buildTree(splitDataset, subLabels)
            tree[bestFeatLabel][value] = subTree
        return tree


