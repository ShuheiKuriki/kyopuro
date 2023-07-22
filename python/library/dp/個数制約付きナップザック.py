'''
    verify:https://paiza.jp/career/challenges/608/retry
    スライド最小値の最大値版
    値とは別に添え字を記録しておくところがポイント
'''
import sys;RL=sys.stdin.readline;I=lambda:map(int,RL().split())
N,X = I()
A = [tuple(I()) for _ in range(N)]
INF = 10**18
dp = [0]+[-INF]*X
from collections import*
for v,w,c in A:
    pdp = [a-w*(i//v) for i,a in enumerate(dp)] # ポテンシャルを表す配列
    for mod in range(v):
        que = deque([])
        for money in range(mod,X+1,v):
            while que and pdp[que[-1]]<pdp[money]:
                que.pop()
            que.append(money)
            dp[money] = pdp[que[0]]+w*((money-mod)//v)
            if que[0]<=money-v*c:
                que.popleft()
print([-1,dp[X]][dp[X]>0])