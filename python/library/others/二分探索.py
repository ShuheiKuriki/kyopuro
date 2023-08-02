def binary_search(low, high, eps=1, get_mini=True):
    #求めるのが最大値か最小値かでokとngが反転
    ok, ng = (high, low-eps) if get_mini else (low, high+eps)
    mid = (ok+ng)/2 if eps<1 else (ok+ng)//2
    while abs(ok-ng)>eps:
        ok, ng = (mid, ng) if is_ok(mid) else (ok, mid)
        mid = (ok+ng)/2 if eps<1 else (ok+ng)//2
    return ok

#判定問題の条件を満たすときTrueを返す関数
def is_ok(target):
    return target

# 単純に下限と上限を指定（広くして損はないので、広めに設定）
low, high = 0, 10**18
res = binary_search(low, high, eps=1, get_mini=False)
print(res)