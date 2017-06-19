import numpy as np

def loadDataSet():
    postingList = [['my', 'dog', 'has', 'flea', 'problems', 'help', 'please'],
                   ['maybe', 'not', 'take', 'him', 'to', 'dog', 'park', 'stupid'],
                   ['my', 'dalmation', 'is', 'so', 'cute', 'I', 'love', 'him', 'my'],
                   ['stop', 'posting', 'stupid', 'worthless', 'garbage'],
                   ['mr', 'licks', 'ate', 'my', 'steak', 'how', 'to', 'stop', 'him'],
                   ['quit', 'buying', 'worthless', 'dog', 'food', 'stupid']]
    classVec = [0, 1, 0, 1, 0, 1]  # 1 is abusive, 0 not
    return postingList, classVec

class NBayes(object):
    def __init__(self):
        self.vocabulary = []   # 词典
        self.idf = 0           # 词典的IDF权值向量
        self.tf = 0            # 训练集的权值矩阵
        self.tdm = 0           # P(x|yi)
        self.Pcates = {}       # P(yi)是一个类别字典
        self.labels = []       # 对应的每个文本的分类，是一个外部导入的列表
        self.doclength = 0     # 训练集文本数
        self.vocablen = 0      # 词典词长
        self.testset = 0       # 测试集

    def train_set(self, trainset, classVec):
        self.cate_prob(classVec)    # 计算每个分类的概率
        self.doclength = len(trainset)
        tempset = set()              # 集合元素不支持索引
        [tempset.add(word) for doc in trainset for word in doc]  # 生成词典   ####!!!!!!!!重点知识
        self.vocabulary = list(tempset)
        self.calc_wordFreq(trainset)     # 计算词频数据集
        self.build_tdm()                # 按分类累计向量空间的每个维度的值P(x|yi)


    def cate_prob(self, classVec):
        self.labels = classVec
        labeltemps = set(self.labels)       # 只包含0 1 两个元素
        for labeltemp in labeltemps:
            # 统计列表中重复的分类self.labels.count(labeltemp)
            self.Pcates[labeltemp] = float(self.labels.count(labeltemp))/float(len(self.labels))
            #  Pcates = {0: 0.5, 1: 0.5}

    # 生成普通的词频向量，没用到TF-IDF策略
    def calc_wordFreq(self, trainset):
        self.idf = np.zeros([1, self.vocablen])
        self.tf = np.zeros([self.doclength, self.vocablen])
        for index in range(self.doclength):     # 遍历所有文本
            for word in trainset[index]:        # 遍历文本中的每个词
                # 找到文本的词在字典的位置+1
                self.tf[index, self.vocabulary.index(word)] += 1
            for signleword in set(trainset[index]):
                # 统计一个词在所有文本中出现的次数
                self.idf[0, self.vocabulary.index(signleword)] += 1

    # 按分类累计向量空间的每维度值P(x|yi)
    def build_tdm(self):
        self.tdm = np.zeros([len(self.Pcates)], self.vocablen)  # 类别行×词典列
        sumlist = np.zeros([len(self.Pcates), 1])  # 统计每个类别的总值
        for index in range(self.doclength):
            #  将同一类别的词向量空间值加总、相同类别的行相加
            self.tdm[self.labels[index]] += self.tf[index]
            # 统计每个分类的总值——是一个标量 、每一行的列相加
            sumlist[self.labels[index]] = np.sum(self.tdm[self.labels[index]])
        self.tdm = self.tdm/sumlist     # 生成P(x|yi)


    # map2vocab函数，将测试集映射到当前词典
    def map2vocab(self, testdata):
        self.testset = np.zeros([1, self.vocablen])
        for word in testdata:
            self.testset[0, self.vocabulary.index(word)] += 1


    # predict函数：预测分类结果，输出预测的分类类别。
    def predict(self, testset):
        if np.shape(testset)[1] != self.vocablen:
            print("输出错误")
            exit(0)
        predvalue = 0
        predclass = ""   #初始化类别概率和类别名称
        for tdm_vect, keyclass in zip(self.tdm, self.Pcates):
            #  P(x|yi) P(yi)
            #  变量tdm, 计算最大分类值
            temp = np.sum(testset*tdm_vect*self.Pcates[keyclass])
            if temp > predvalue:
                predvalue = temp
                predclass = keyclass
        return predclass


# 使用TF-IDF策略的词频向量
    def calc_tfidf(self, trainset):
        self.idf = np.zeros([1, self.vocablen])
        self.tf = np.zeros([self.doclength, self.vocablen])
        for index in range(self.doclength):
            for word in trainset[index]:
                self.tf[index, self.vocabulary.index(word)] += 1
            # 消除不同句长导致的偏差
            self.tf[index] = self.tf[index]/float(len(trainset[index]))

            for signleword in set(trainset[index]):
                self.idf[0, self.vocabulary.index(signleword)] += 1

        self.idf = np.log(float(self.doclength)/self.idf)
        self.tf = np.dot(self.tf, self.idf)
















