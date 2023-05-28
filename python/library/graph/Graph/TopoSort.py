"""
トポロジカルソートしてorderを定めてからdpする
グラフ条件:DAG(有向非巡回グラフ、閉路がなく根が分かっていない)
"""
import sys;RL=sys.stdin.readline;I=lambda:map(int,RL().split())
from collections import*
class Graph:
    def __init__(self, N, M=-1):
        self.V = N
        if M>=0: self.E = M
        self.edge = [[] for _ in range(self.V)]
        self.edge_rev = [[] for _ in range(self.V)]
        self.order = []
        self.to = [0]*self.V
        self.dp = [0]*self.V

    def add_edges(self, ind=1):
        for a,*A in [tuple(I()) for _ in range(self.E)]:
            a -= ind; b = A[0] - ind
            atob,btoa = (b,a) if len(A) == 1 else ((A[1],b),(A[1],a))
            self.edge[a].append(atob)
            self.edge_rev[b].append(btoa)
            self.to[b] += 1

    def add_edge(self, a, b, cost=None, ind=1):
        a -= ind; b -= ind
        atob,btoa = (b,a) if cost is None else ((cost,b),(cost,a))
        self.edge[a].append(atob)
        self.edge_rev[b].append(btoa)
        self.to[b] += 1

    def topo_sort(self):
        # トポロジカルソート
        updated = [0]*self.V
        for start in range(self.V):
            if self.to[start] or updated[start]: continue
            que = deque([start])
            while que:
                v = que.popleft()
                self.order.append(v)
                updated[v] = 1
                for u in self.edge[v]:
                    self.to[u] -= 1
                    if self.to[u] > 0: continue
                    que.append(u)

    def dfs_dp(self):
        # トポソしてorderを定めてからdp
        self.topo_sort()
        # 行きがけ(pre_order)
        for v in self.order:
            #配るDP
            for u in self.edge[v]:
                self.dp[u] = max(self.dp[u], self.dp[v]+1)
        # 帰りがけ(post_order)
        for v in self.order[::-1]:
            #配るDP
            for u in self.edge_rev[v]:
                self.dp[u] = max(self.dp[u], self.dp[v]+1)

N, M = I()
G = Graph(N,M)
G.add_edges(ind=0)
G.topo_sort()
print(*G.order, sep="\n")