with open ('testSet.txt') as f1, open('newtestSet.txt','w') as f2:
    for line in f1:
        f2.write(','.join(line.split())+'\n')

#将每一行的字符串断开用逗号重连，并加入换行符