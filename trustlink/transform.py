from numpy import *

def transformNetworks(Networks):
    result = {}
    for network in Networks:
        leaders = Networks[network]['leader']
        followers = Networks[network]['follower']
        for follower in followers:
            result.setdefault(follower, [])    # 很重要的用法
            result[follower].append(leaders)
    print("the transformed matrix is as follow:")
    print(result)
    # 去除leader中的重复值
    # for newwork in result:
    #     result[newwork] = set(result[newwork])

    return result





