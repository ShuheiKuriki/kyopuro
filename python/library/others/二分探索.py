class Bisearch:
    def __init__(self, func=None):
        self.func = func
    
    def binary_search(self, low, high, func=None, mini=True):
        #求めるのが最大値か最小値かでokとngが反転
        if mini: ok, ng = high, low-1
        else:    ok, ng = low, high+1
        if func is None: func = self.func

        mid = (ok+ng)//2
        while abs(ok-ng)>1:
            if func(mid): ok = mid
            else: ng = mid
            mid = (ok+ng)//2
        return ok

#判定問題の条件を満たすときTrueを返す関数
def is_ok(target):
    return target

B = Bisearch(is_ok)
# 単純に下限と上限を指定
low, high = 2, 10**18
res = B.binary_search(low,high,mini=False)
print(res)