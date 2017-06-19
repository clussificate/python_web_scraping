from numpy import *
import numpy as np
import xlrd
def matread(filename):
    data = xlrd.open_workbook(filename)
    table = data.sheets()[0]
    nrows = table.nrows
    ncols = table.ncols
    myarr = np.zeros([nrows-1, ncols-1])
    for i in range(nrows - 1):
        myarr[i] = table.row_values(i + 1)[1:]
    return myarr


def myformat(mat):
    for i in range(mat.shape[0]):
        mat[i][i]=0
    return mat

def countDegree(mat):
    outdegree = zeros([1, mat.shape[0]])
    indegree = zeros([1, mat.shape[0]])
    sumdegree = zeros([1, mat.shape[0]])
    # 出度数
    for index in range(len(mat)):
        for degree in mat[index]:
            if degree != 0 and degree != 1:
                outdegree[0][index] += 1
    #入度数
    for index in range(len(mat)):
        for degree in mat[:,index]:
            if degree != 0 and degree != 1:
                indegree[0][index] += 1

    #总度数
    sumdegree = outdegree + indegree
    return sumdegree


def cheak(mat, t):
    a = 1
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            if mat[i, j] >= t:
                a = 0
                break
    return a
# t表示阈值
def aggrenodes(mat, t):
    mylist = []
    while True:
        # 判断循环式否结束：
        mat2 = myformat(mat)
        if cheak(mat2, t):
            break

        sumdegree = countDegree(mat)
        rankdegreeind = argsort(sumdegree)
        for index in rankdegreeind[0]:
            if sumdegree[0, index] == 0:  #删除的节点跳过
                continue
            maxRindex = 0   # 最大值的行索引
            maxCindex = 0   # 最大值的列索引
            maxindex = 0    #最大值索引
            maxr = 0
            maxc = 0
            maxs = 0
            for jr in range(len(mat[index])):   # 求行最大值
                if mat[index][jr] > maxr and mat[index][jr] != 1:
                    maxr = mat[index][jr]
                    maxRindex = jr
            for jc in range(len(mat[:, index])):   # 求列最大值
                if mat[jc][index] > maxc and mat[jc][index] != 1:
                     maxc = mat[jc][index]
                     maxCindex = jc
            # 判断出度入度的大小，若最大值在出度，且大于阈值t，则该节点并入对象
            if maxr >= maxc:
                maxindex = maxRindex
                maxs = maxr
                if maxs >= t:
                    mat[index, :] = 0
                    mat[:, index] = 0
                    print('delete node：',index+1,'join to：',maxindex+1)
                    mylist.append([index+1, maxindex+1])
    print('final matrix:', mat)
    return mylist

def classifynodes(mylist):
    b = len(mylist)
    for i in range(b):
        for j in range(b):
            x = list(set(mylist[i] + mylist[j]))
            y = len(mylist[j]) + len(mylist[i])
            if i == j or mylist[i] == 0 or mylist[j] == 0:
                break
            elif len(x) < y:
                mylist[i] = x
                mylist[j] = [0]
    finallist = []
    for i in mylist:
        if i != [0]:
            finallist.append(i)
    return finallist


def findisolated(mylist, mymat):
    matlen = len(mymat)
    nodes = list(range(1, matlen+1))
    isolatednodes = []
    for i in nodes:
        check = True
        for j in range(len(mylist)):
            for k in mylist[j]:
                if i == k:
                    check = False
        if check == True:
            isolatednodes.append(i)
    return isolatednodes


# test_case
# a1 = [1, 0, 0, 0, 0.5, 0, 0]
# a2 = [0, 1, 0, 0.7, 0, 0, 0]
# a3 = [0, 0, 1, 0.6, 0, 0.6, 0]
# a4 = [0, 0, 0, 1, 0.6, 0.5, 0]
# a5 = [0, 0.6, 0, 0.6, 1, 0.6, 0]
# a6 = [0, 0, 0, 0.8, 0, 1, 0.6]
# a7 = [0, 0, 0, 0, 0.5, 0, 1]
# mat = array([a1, a2, a3, a4, a5, a6, a7])
# mat =  array([[ 1. ,  0.6,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,
#          0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
#        [ 0. ,  1. ,  0.7,  0. ,  0.8,  0. ,  0.7,  0. ,  0.4,  0. ,  0. ,
#          0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
#        [ 0. ,  0. ,  1. ,  0. ,  0.6,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,
#          0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
#        [ 0. ,  0. ,  0. ,  1. ,  0. ,  0.5,  0. ,  0. ,  0. ,  0. ,  0.6,
#          0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
#        [ 0. ,  0. ,  0. ,  0. ,  1. ,  0. ,  0. ,  0. ,  0. ,  0.6,  0. ,
#          0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
#        [ 0. ,  0. ,  0. ,  0. ,  0. ,  1. ,  0. ,  0. ,  0. ,  0. ,  0. ,
#          0.3,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
#        [ 0. ,  0.6,  0. ,  0. ,  0. ,  0. ,  1. ,  0. ,  0. ,  0.8,  0. ,
#          0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
#        [ 0. ,  0.6,  0. ,  0. ,  0. ,  0. ,  0. ,  1. ,  0.6,  0. ,  0. ,
#          0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
#        [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  1. ,  0.7,  0. ,
#          0. ,  0. ,  0.6,  0. ,  0. ,  0. ,  0. ,  0. ],
#        [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  1. ,  0.6,
#          0. ,  0. ,  0.4,  0. ,  0. ,  0. ,  0. ,  0. ],
#        [ 0. ,  0. ,  0. ,  0. ,  0. ,  0.6,  0. ,  0. ,  0. ,  0.5,  1. ,
#          0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
#        [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0.6,  0. ,
#          1. ,  0. ,  0. ,  0.6,  0. ,  0. ,  0. ,  0. ],
#        [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0.8,  0.6,  0. ,  0. ,
#          0. ,  1. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ],
#        [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0.7,  0.3,  0. ,
#          0. ,  0. ,  1. ,  0. ,  0. ,  0. ,  0. ,  0. ],
#        [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,
#          0. ,  0. ,  0.6,  1. ,  0. ,  0.3,  0. ,  0. ],
#        [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,
#          0. ,  0. ,  0. ,  0.5,  1. ,  0. ,  0. ,  0. ],
#        [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,
#          0. ,  0. ,  0.6,  0. ,  0. ,  1. ,  0. ,  0. ],
#        [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,
#          0. ,  0. ,  0. ,  0.6,  0. ,  0.7,  1. ,  0. ],
#        [ 0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,  0. ,
#          0. ,  0. ,  0.7,  0. ,  0. ,  0. ,  0. ,  1. ]])

filename = 'data1.xlsx'
mat = matread(filename)
sumdegree = countDegree(mat)
mylist = aggrenodes(mat, 0.6)
finallist = classifynodes(mylist)
print('Final results as follow:')
print(finallist)
isonodes = findisolated(finallist, mat)
print('the isolated nodes as follow: ')
print(isonodes)






















