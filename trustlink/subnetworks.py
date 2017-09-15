from numpy import *


# Warshall算法得出可达矩阵
def Warshall(matrix):
    Accmat = mat(matrix)
    n = len(Accmat)
    for i in range(n):
        Accmat[i,i]=1
    for k in range(n):
        for i in range(n):
            for j in range(n):
              Accmat[i,j]=Accmat[i,j] or (Accmat[i,k] and Accmat[k,j])
    print("可达矩阵：")
    print(Accmat)
    return Accmat

def SubNetSplit(Accmat):
    netsplit = {}
    count = 1
    n = len(Accmat)
    v = list(range(1,n+1))
    v0 = []
    for i in range(n):
        for j in range(n):
            if Accmat[i,j]==1 and Accmat[j,i]==0:
                v0.append(i+1)
                break

    vcopy1 = v.copy()
    for k in v0:
        vcopy1.remove(k)
    v1 = vcopy1.copy()

    while len(v1)!=0:
        # 找出leader节点
        for t in v1:
            v_leader = []
            v_follower = []
            v_leader.append(t)
            for j in v1:
                if Accmat[t-1,j-1] == 1 and Accmat[j-1,t-1] == 1 and t != j :   # 注意下标
                    v_leader.append(j)

            # 找出follower节点
            for i in v_leader:
                for j in v0:
                    if Accmat[j-1,i-1] == 1 and j not in v_follower:
                        v_follower.append(j)

            v_net={"leader":v_leader,"follower":v_follower}
            print('iter % s :' % count)
            print("the leaders are:",v_leader)
            print("the followers are:",v_follower)
            print("the subnetwork is",v_net)
            netsplit['% s' % count] = v_net
        # 更新v1   与原算法不同，每次找到一个leader后，在下次迭代需要删除前面的leader.

            for k in v_leader:
                if k in v1:
                    v1.remove(k)

            # 判断V1是否为空，空的话跳出迭代过程
            count = count+1

    print('the network partition is as follow:')
    print(netsplit)
    return netsplit,count


if __name__=="__main__":

    # example = mat([[0,1,0,0,0],
    #                [0,0,0,1,0],
    #                [0,0,0,0,1],
    #                [1,0,1,0,1],
    #                [0,0,1,0,0]
    #                ])
    # AccMat = Warshall(example)
    # NetPar, count= SubNetSplit(AccMat)
    # print("iterations is: ",count)
    example2 = mat([[0, 1, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 1, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 1, 1, 0, 0, 1],
                    [1, 0, 1, 0, 1, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 1, 0, 1, 0],
                    [0, 0, 0, 0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0]
                    ])
    AccMat2 = Warshall(example2)
    Netpar2, count2 = SubNetSplit(AccMat2)
