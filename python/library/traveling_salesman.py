#dp[既に訪れた頂点の集合][現在の頂点]
#配るDP
#スタートは既に訪れた頂点に含まない
#既にスタートを訪れている場合は考える必要がない

def solve():
    V, E = map(int, input().split())
    edge = [[] for _ in range(V)]
    for i in range(E):
        s,t,d = map(int, input().split())
        edge[s].append([t,d])
    dp = [[float('inf')]*V for _ in range(1<<V)]
    for v,d in edge[0]:
        dp[1<<v][v] = min(dp[1<<v][v],d)
    for S in range(2,1<<V,2):
        for u in range(V):
            if (S>>u)&1:
                for v,d in edge[u]:
                    if not (S>>v)&1:
                        dp[S+(1<<v)][v] = min(dp[S+(1<<v)][v],dp[S][u]+d)
    return dp[-1][0] if dp[-1][0]<float('inf') else -1
print(solve())