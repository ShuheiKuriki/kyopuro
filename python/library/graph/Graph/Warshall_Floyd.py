import sys;RL=sys.stdin.readline;I=lambda:map(int,RL().split())
# ワーシャルフロイド法、計算量O(N^3)
N, M = I()
INF = 10**18
d = [[INF]*N for _ in range(N)]
for i in range(M): #ひとまず枝があるペアは枝の長さをセット
    a,b,t = I()
    d[a-1][b-1] = t
    d[b-1][a-1] = t

for i in range(N):
    d[i][i] = 0 #自身への最短経路は0
#三重ループ
for k in range(N):
    for i in range(N):
        for j in range(N):
            d[i][j] = min(d[i][j], d[i][k]+d[k][j])
