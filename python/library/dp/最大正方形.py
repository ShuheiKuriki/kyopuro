# 最大正方形
# https://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=DPL_3_A
import sys;RL=sys.stdin.readline;I=lambda:map(int,RL().split())
H,W = I()
A = [tuple(I())for _ in range(H)]
dp = [[0]*(W+1)for _ in range(H+1)]
for h in range(H):
    for w in range(W):
        if A[h][w]==0:
            dp[h+1][w+1] = min(dp[h][w],dp[h+1][w],dp[h][w+1])+1
print(max(max(dp[h])for h in range(H+1))**2)