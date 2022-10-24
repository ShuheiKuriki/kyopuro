"""
dfsの訪問順でdpする
グラフ条件:根が分かっている、有向も無向も想定
"""
import sys; input = sys.stdin.readline
I = lambda:map(int,input().split())
class Graph:
    def __init__(self, N, M=-1):
        self.V = N
        if M>=0: self.E = M
        self.edge = [[] for _ in range(self.V)]

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

    def dp_dfs(self, start):
        stack = [start]
        self.parent = [self.V]*self.V; self.parent[start] = -1
        self.order = [start]
        self.dp = [1]*self.V
        while stack:
            # 行きがけ(pre-order)
            v = stack.pop()
            for u in self.edge[v]:
                if u==self.parent[v]: continue
                self.parent[u]=v
                stack.append(u); self.order.append(u)
        for v in self.order[::-1]:
            # 帰りがけ(post-order)
            for u in self.edge[v]:
                if u==self.parent[v]: continue
                self.dp[v] += self.dp[u]

N, M = I()
G = Graph(N,M)
G.add_edges(ind=1, bi=False)
G.dp_dfs(0)