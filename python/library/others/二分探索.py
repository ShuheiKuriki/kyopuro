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
    lA = sorted((1-target)*x-target*y for x,y in AB)
    lC = sorted((1-target)*x-target*y for x,y in CD)
    j = M
    cnt = 0
    for i in range(N):
        while j > 0 and lA[i] + lC[j-1] >= 0:
            j -= 1
        cnt += M-j
    return cnt >= K

import sys;RL=sys.stdin.readline
I=lambda:map(int,RL().split())
N,M,K = I()
AB = [tuple(I()) for _ in range(N)]
CD = [tuple(I()) for _ in range(M)]
# 単純に下限と上限を指定
low, high = 0, 1
res = binary_search(low, high, eps=1e-10, get_mini=False)
print(res*100)