from numpy import *
import numpy as np
import pandas as pd

u_cols = ['user_id', 'item_id', 'rating', 'timestrap']
ratings = pd.read_csv('D:/ml-100k/u.data',sep='\t',names=u_cols)
u_cols = ['user_id', 'age', 'gender', 'occpation', 'zipcode']
users = pd.read_csv('D:/ml-100k/u.user',sep='|',names=u_cols)
u_cols = ['item_id','movie_title', 'release_date', 'video release date','IMDb URL','unknown','Action','Advent ure',\
          'Animation','Children','Comedy','Crime','Documentary','Drama','Fantasy','Film-Noir','Horror','Musical',\
          'Mystery','Romance','Sci-Fi','Thriller','War','Western']
movies = pd.read_csv('D:/ml-100k/u.item',sep='|',names=u_cols)
movies_ratings=pd.merge(ratings,movies,left_on='item_id',right_on='item_id')
# 可定义一个函数
ratmat=np.zeros((943,1682))
df2 = movies_ratings[movies_ratings.Action==1]  #动作类电影
movielist = df2['item_id'].tolist()
userlist = df2.user_id.tolist()
results=[]
for i in range(len(userlist)):
    x=userlist[i]
    y=movielist[i]
    ratmat[x-1,y-1]=1
for i in range(len(ratmat)):
    for j in range(i+1,len(ratmat)):
        a=sum(ratmat[i]*ratmat[j])
        if a>=100:
            results.append([x, y, a])


# m = len(set(userids))
# n = len(set(movie_ids))
# lalmat=zeros((m,n))
# ratmat=np.zeros((943,1682)) # 评分矩阵
### 取每一行的userid 和itemiｄ
# for i in range(len(df2)):
#     x=df2.iloc[i,0]
#     y=df2.iloc[i,1]

#  moviecounts = len(movie_ids)
#
#
#
# ralmat=zeros((moviecounts,moviecounts))

