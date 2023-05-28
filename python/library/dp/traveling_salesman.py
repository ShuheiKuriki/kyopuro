# https://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=DPL_2_A&lang=ja
#dp[既に訪れた頂点の集合][現在の頂点]
#配るDP
#スタートは既に訪れた頂点に含まない
#既にスタートを訪れている場合は考える必要がない
import sys;RL=sys.stdin.readline;I=lambda:map(int,RL().split())
V, E = I()
edge = [[] for _ in range(V)]
for i in range(E):
    u,v,d = I()
    edge[u].append((v,d))
s = 0
INF = 10**18
dp = [[INF]*V for _ in range(1<<V)]
for v,d in edge[s]: dp[1<<v][v] = min(dp[1<<v][v],d)
for bit in range(1,1<<V):
    if (bit>>s)&1:continue
    # v：現在の頂点（集合に含まれる）
    # u：次に訪れる頂点（集合に含まれない）
    for v in range(V):
        if (bit>>v)&1==0: continue
        for u,d in edge[v]:
            if (bit>>u)&1: continue
            dp[bit|(1<<u)][u] = min(dp[bit|(1<<u)][u],dp[bit][v]+d)
ans = dp[-1][0] if dp[-1][0]<INF else -1
print(ans)