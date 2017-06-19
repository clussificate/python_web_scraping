import numpy as np
import math
import scipy.spatial.distance as dist
vector1 = np.array([1, 2, 3])
vector2 = np.array([4, 5, 7])
#欧式距离
l=np.dot((vector1-vector2),(vector1-vector2).T)
print(math.sqrt(l))
print(math.sqrt(sum(np.power(vector1-vector2, 2))))

#曼哈顿距离
print(sum(abs(vector1-vector2)))
#切比雪夫距离
print(max(abs(vector1-vector2)))
#夹角余弦  dot表示点乘
print((np.dot(vector1, vector2.T))/(math.sqrt(np.dot(vector1, vector1.T)*np.dot(vector2, vector2.T))))
#杰卡德距离 Jaccard dist.
print(dist.pdist(np.array(vector1, vector2),'jaccard'))
