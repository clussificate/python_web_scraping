from numpy import *
from trustlink import ShortestPath
from trustlink import transform
from trustlink import subnetworks
from trustlink import matread
#follower到所有次网络leaders的平均距离
def computetrust(follower, leaders):
    grouptrust = 0
    grouplength = []
    for leader in leaders:
        trust = 1
        dist, Shortest_path = ShortestPath.dijkstra(edges, follower, leader)
        for i, value in enumerate(Shortest_path):
            if i != len(Shortest_path)-1:
                valuenew = Shortest_path[i + 1]
                trustnew = TrustMat[value - 1, valuenew - 1]
                trust = trust*trustnew
        grouptrust = grouptrust+trust
        grouplength.append(len(Shortest_path))
    avetrust = grouptrust/len(leaders)
    minlength = min(grouplength)
    return avetrust, minlength


# 遍历每个follower. 输入一个字典
def FindOptimalSubNet(edges,NetworkDict,lam):
    for i in NetworkDict:
        distance = 0
        minlens = []
        avetrusts = []
        for item in NetworkDict[i]:
            avetrust, minlength = computetrust(i, item)
            minlens.append(minlength)
            avetrusts.append(avetrust)
            if avetrust >= distance:
                distance = avetrust
                NetworkDict[i] = item
        if max(avetrusts)<lam:
            NetworkDict[i]='isolated'
        if min(minlens)>6:
            NetworkDict[i]='isolated'
    return NetworkDict


if __name__ == "__main__":
    global TrustMat
    global edges
    global AdjMat

  # 读取信任矩阵和邻接矩阵
    filename2 = 'D:/python_web_scraping/trustlink/TruMat.xlsx'
    TrustMat = matread.read_excel(filename2)
    filename = 'D:/python_web_scraping/trustlink/AdjMat.xlsx'
    AdjMat = matread.read_excel(filename)


#   根据邻接矩阵，得出次网络，并转换为follower:leaders形式

    AccMat2 = subnetworks.Warshall(mat(AdjMat))
    Netpar2, count = subnetworks.SubNetSplit(AccMat2)
    trf = transform.transformNetworks(Netpar2)

#   根据信任矩阵，求出每个follower到leader groups的信任值
    Stmat1 = ShortestPath.Stdmat(TrustMat)   # distrust matrix
    edges = ShortestPath.findedges(Stmat1)   # 计算edges
    lam = 0.5  #  阈值
    OptimalNet = FindOptimalSubNet(edges,trf,lam)
    print("the finally subnetworks is :\n", OptimalNet)

