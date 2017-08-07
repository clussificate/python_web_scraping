from numpy import *
from collections import defaultdict
from heapq import *

# 对矩阵预处理
def Stdmat(PathMat, M=9999):
    PathMat = mat(PathMat)
    # 将信任矩阵转换为不信任矩阵
    PathMat = 1 - PathMat
    n = len(PathMat)
    for i in range(n):
        for j in range(n):
            if i==j:
                PathMat[i,j]=M
            if PathMat[i,j]==1:
                PathMat[i,j]= M
    return PathMat

#  根据连接矩阵找到连接边
def findedges(Stmat1,M=9999):
    edges = []
    for i in range(len(Stmat1)):
        for j in range(len(Stmat1)):
            if Stmat1[i, j] != M:
                edges.append(
                    (i, j, Stmat1[i, j]))  ### (i,j) is a link; Stmat1[i][j] here is 1, the length of link (i,j).
    return edges

def dijkstra_raw(edges, from_node, to_node):
    g = defaultdict(list)
    for l, r, c in edges:
        g[l].append((c, r))
    q, seen = [(0, from_node, ())], set()
    while q:
        (cost, v1, path) = heappop(q)
        if v1 not in seen:
            seen.add(v1)
            path = (v1, path)
            if v1 == to_node:
                return cost, path
            for c, v2 in g.get(v1, ()):
                if v2 not in seen:
                    heappush(q, (cost + c, v2, path))
    return float("inf"), []


def dijkstra(edges, from_node, to_node):
   # to get the true index of nodes
    from_node=from_node-1
    to_node = to_node-1

    len_shortest_path = -1
    ret_path = []
    length, path_queue = dijkstra_raw(edges, from_node, to_node)
    if len(path_queue) > 0:
        len_shortest_path = length  ## 1. Get the length firstly;
        ## 2. Decompose the path_queue, to get the passing nodes in the shortest path.
        left = path_queue[0]
        ret_path.append(left)  ## 2.1 Record the destination node firstly;
        right = path_queue[1]
        while len(right) > 0:
            left = right[0]
            ret_path.append(left)  ## 2.2 Record other nodes, till the source-node.
            right = right[1]
        ret_path.reverse()  ## 3. Reverse the list finally, to make it be normal sequence.  反转
    NodeIndex = array(ret_path)+1 # return the true index of node
    return len_shortest_path, NodeIndex
if __name__ == "__main__":
    test = array([[1, 0.8, 0, 0.6], [0.6, 1, 0.7, 0], [0, 0.8, 1, 0.7], [0.8, 0, 0, 1]])
    list_nodes_id = list(range(len(test)))
    M = 9999
    Stmat1 = Stdmat(test, M)
    print("the distrust matrix is:")
    print(Stmat1)
    edges = findedges(Stmat1)

    # 输入部分
    length, Shortest_path = dijkstra(edges, 3, 4)
    print('length = ', length)
    print('The shortest path is ', Shortest_path)

