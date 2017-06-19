from numpy import *
def loadDataSet(filename):
    dataMat = []; labelmat=[]
    with open(filename) as fr:
        for line in fr.readlines():
            lineArr = line.strip().split('/t')
            dataMat.append([float(lineArr[0]), float(lineArr[1])])
            labelmat = labelmat.append(float(lineArr[2]))
    return dataMat,labelmat
# 随机选择与alpha i对应的alpha j, 正式选择一般是考虑i，j样本的欧氏距离，选择差异最大的
def selectJrand(i, m):
    j=i
    while(j==i):
        j=int(random.uniform(0,m))
    return j
# 判断alpha大小是否在（L,H）范围内
def clipAlpha(aj, H, L):
    if aj>H: aj=H
    if aj<L: aj=L
    return aj

# SMO算法简易版
# 创建一个alpha向量并将其初始化为0向量
# 当迭代次数小于最大迭代次数时（外循环）：
#   对数据集每一个数据向量（内循环）：
#      如果该数据向量可以被优化：
#         随机选择另外一个数据向量
#         同时优化这两个向量
#         如果两个向量都不能被优化，退出内循环
#  如果所有的向量都不能被优化，增加迭代次数，继续下一轮循环

def smoSimple(datamatIn, classLabels, C, toler, maxIter):  # toler 容错率
    dataMatrix = mat(datamatIn); labelMat = mat(classLabels).T
    b=0; m,n = shape(dataMatrix)
    alphas = mat(zeros((m,1)))
    iter = 0
    while(iter<maxIter):
        alphaPairsChanged = 0    # 记录alpha是否改变
        for i in range(m):
            fxi = float(multiply(alphas, labelMat).T * (dataMatrix * dataMatrix[i, :].T)) + b
            Ei = fxi - float(labelMat[i])
            # 如果alpha可以更改进入优化过程
            if ((labelMat[i] * Ei < - toler) and (labelMat[i] < C)) or ((labelMat[i]*Ei>toler) and (labelMat[i] > 0)):
                j = selectJrand(i,m)
                fxj = float(multiply(alphas,labelMat).T*(dataMatrix*dataMatrix[j,:].T))+b
                Ej = fxj - float(labelMat[j])
                alphaIold = alphas[i].copy()
                alphaJold = alphas[j].copy()
                if (labelMat[i]!=labelMat[j]):
                    L = max(0, alphas[j]-alphas[i])
                    H = min(C,C + alphas[j]-alphas[i])
                else:
                    L = max(0, alphas[j]+alphas[i]-C)
                    H = min(C, alphas[j]+alphas[i])
                if L==H: print('L==H'); continue
                eta = 2.0 * dataMatrix[i,:] * dataMatrix[j,:].T - dataMatrix[i,:]*dataMatrix[i,:].T - \
                    dataMatrix[j,:]*dataMatrix[j,:].T
                if eta>=0: print("eta=0"); continue
                alphas[j] -=labelMat[j]*(Ei-Ej)/eta
                alphas[j]=clipAlpha(alphas[j],H,L)
                if (abs(alphas[j]-alphaJold)<0.00001): print('j not moving enouth'); continue
                # 对i进行修改，修改量与j相同，但方向相反
                alphas[i]+=labelMat[i]*labelMat[j]*(alphaJold-alphas[j])
                b1 = b - Ei - labelMat[i]*(alphas[i]-alphaIold) * dataMatrix[i,:]*dataMatrix[i,:].T - \
                    labelMat[j]*(alphas[j]-alphaJold)*dataMatrix[i,:]*dataMatrix[j,:].T
                b2 = b - Ei - labelMat[i] * (alphas[i] - alphaIold) * dataMatrix[i, :] * dataMatrix[j, :].T - \
                     labelMat[j] * (alphas[j] - alphaJold) * dataMatrix[j, :] * dataMatrix[j, :].T
                if(0<alphas[i]) and (C > alphas[i]): b = b1
                elif (0<alphas[j]) and (C>alphas[j]): b = b2
                else: b = (b1+b2)/2.0
                alphaPairsChanged += 1
                print("iter: %d i: %d, pairs changed %d" % (iter, i, alphaPairsChanged))
        if(alphaPairsChanged == 0): iter += 1
        else:iter = 0
        print('iteration number: %d' % iter)
    return b, alphas








