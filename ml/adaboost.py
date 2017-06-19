from numpy import *
def loadSimpData():
    datamat = matrix([[1.0, 2.1], [2., 1.1], [1.3, 1.], [1., 1.], [2., 1.]])
    classlabels = [1.0, 1.0, -1.0, -1.0, 1.0]
    return datamat, classlabels

# build decison stump
def stumpClassify(dataMatrix, dimen, threshVal, threshIneq):   # threshIneq决定根据左树还是右数划分
    retArray = ones((shape(dataMatrix)[0], 1))
    if threshIneq == 'lt':  # 根据左树来划分，小于阈值的设为-1类
        retArray[dataMatrix[:, dimen] <= threshIneq] = -1.0
    else:
        retArray[dataMatrix[:, dimen] > threshIneq] = -1.0
    return retArray

def buildStump(dataArr, classLabels,D):  # D是每个样本的权重向量,
                                          # 输出一个最优的决策树桩（所有属性都考虑了）
    datamatrix= mat(dataArr); labelmat = mat(classLabels).T
    m, n = shape(datamatrix)
    numstep = 10.0; bestStump = {}; bestClassEst = mat(zeros(m, 1))
    minError = inf
    for i in range(n):
        rangeMin = datamatrix[:, i].min(); rangeMax = datamatrix[:, i].max()
        stepsize=(rangeMax-rangeMin)/numstep
        for j in range(-1,int(numstep+1)):  # 阈值可以设在取值范围之外
            for inequal in ['lt','gt']:
                threshval = (rangeMin + float(j)*stepsize)
                predictedVals = stumpClassify(datamatrix, i, threshval, inequal)
                errArr = mat(ones(m, 1))
                errArr[predictedVals==labelmat] = 0 # 预测值与真实值一致则取0， 否则取1
                weightedError = D.T * errArr  # 计算加权错误率
                print("split: dim %d, thresh %.2f, thresh ineqal: %s, the weighted error is %.3f" \
                      % (i, threshval, inequal, weightedError)) # 占位符：s 字符串,d 整数，f 浮点数
                if weightedError<minError:
                    minError = weightedError
                    bestClassEst = predictedVals.copy()
                    bestStump['dim']=i
                    bestStump['thresh']=threshval
                    bestStump['ineq']=inequal
    return bestStump,minError,bestClassEst

def adaBoostTrainDs(dataArr, classlabels, numIt=40):
    weakClassArr = []
    m = shape(dataArr)[0]
    D = mat(ones((m,1))/m)
    aggClassEst = mat(zeros((m,1)))
    for i in range(numIt):
        bestStump, error, classEst = buildStump(dataArr, classlabels, D)
        print("D:", D.T)
        alpha = float(0.5*log((1-error)/max(error,1e-16)))  # 计算当前分类器的权重,alpha
        bestStump['alpha'] = alpha
        weakClassArr.append(bestStump)
        print('classEst: ', classEst.T)
        expon = multiply(-1*alpha*mat(classlabels).T, classEst)
        D=multiply(D, exp(expon))
        D = D/D.sum()                                      # 以上三句，求更新后的D

        aggClassEst += alpha*classEst
        print("aggClassEst:", aggClassEst.T)
        aggErrors = multiply(sign(aggClassEst) != mat(classlabels).T, ones((m,1)))
        errorRate = aggErrors.sum()/m
        print('total error:',errorRate,"\n")
        if errorRate == 0.0: break
    return weakClassArr

# AdaBoost分类函数
def AdaClassify(datToclass, classifierArr):
    dataMatrix = mat(datToclass)
    m = shape(dataMatrix)[0]
    aggclassEst = mat(zeros((m, 1)))
    for i in range(len(classifierArr)):    # 遍历每个弱分类器投票，并集成所有结果
        classEst = stumpClassify(dataMatrix,classifierArr[i]['dim'],\
                                    classifierArr[i]['thresh'],classifierArr[i]['ineq'])
        aggclassEst += classEst[i]['alpha']*classEst
        print(aggclassEst)

    return sign(aggclassEst)



