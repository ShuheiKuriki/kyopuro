"""
dfsの訪問順でdpする
グラフ条件:根が分かっている、有向も無向も想定
pythonは再帰処理が遅いので最終手段
"""
import sys; input = sys.stdin.readline
I = lambda:map(int,input().split())
sys.setrecursionlimit(10**6)
class Graph:
    def __init__(self, N, M=-1):
        self.V = N
        if M>=0: self.E = M
        self.edge = [[] for _ in range(self.V)]
        self.visited = [False]*self.V
        self.dp = [0]*self.V

    def add_edges(self, ind=1, bi=False):
        for a,*A in [tuple(I()) for _ in range(self.E)]:
            a -= ind; b = A[0] - ind
            atob,btoa = (b,a) if len(A) == 1 else ((A[1],b),(A[1],a))
            self.edge[a].append(atob)
            if bi: self.edge[b].append(btoa)

    def add_edge(self, a, b, cost=None, ind=1, bi=False):
        a -= ind; b -= ind
        atob,btoa = (b,a) if cost is None else ((cost,b),(cost,a))
        self.edge[a].append(atob)
        if bi: self.edge[b].append(btoa)

    def dp_dfs_rec(self, v):
        if self.visited[v]: return self.dp[v]
        self.visited[v] = True
        for u in self.edge[v]:
            # 行きがけ
            self.dp[u] += self.dp[v]
            # 帰りがけ
            self.dp[v] += self.dp_dfs_rec(u)
        return self.dp[v]

N, M = I()
G = Graph(N,M)
G.add_edges(ind=1, bi=False)
G.dp_dfs_rec(0)