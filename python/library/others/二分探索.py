def binary_search(low, high, func, get_mini=True):
    #求めるのが最大値か最小値かでokとngが反転
    if get_mini:    ok, ng = high, low-1
    else:           ok, ng = low, high+1

    mid = (ok+ng)//2
    while abs(ok-ng)>1:
        if func(mid):   ok = mid
        else:           ng = mid
        mid = (ok+ng)//2
    return ok

#判定問題の条件を満たすときTrueを返す関数
def is_ok(target):
    return target

# 単純に下限と上限を指定
low, high = 2, 10**18
res = binary_search(low,high,is_ok,get_mini=False)
print(res)