"""
ベルマンフォード法：負の重み、負閉路検出可能、計算量O(VE)
https://onlinejudge.u-aizu.ac.jp/courses/library/5/GRL/1/GRL_1_B
"""
import sys; input = sys.stdin.readline
I = lambda:map(int,input().split())
INF = 10**18
class BellmanFord:
    def __init__(self, N, M=-1):
        self.V = N
        if M >= 0: self.E = M
        self.edge = [[] for _ in range(self.V)]

    def add_edges(self, ind=1, bi=False):
        for a,*A in [list(I()) for _ in range(self.E)]:
            a -= ind; b = A[0] - ind
            atob,btoa = (b,a) if len(A) == 1 else ((A[1],b),(A[1],a))
            self.edge[a].append(atob)
            if bi: self.edge[b].append(btoa)

    def add_edge(self, a, b, cost=None, ind=1, bi=False):
        a -= ind; b -= ind
        atob,btoa = (b,a) if cost is None else ((cost,b),(cost,a))
        self.edge[a].append(atob)
        if bi: self.edge[b].append(btoa)

    def bellman_ford(self, s):
        self.dists = [INF]*self.V
        self.dists[s] = 0
        for _ in range(self.V):
            for v in range(self.V):
                for d,u in self.edge[v]:
                    self.dists[u] = min(self.dists[u], self.dists[v]+d)
        for v in range(self.V):
            for d,u in self.edge[v]:
                # まだ最短経路を更新できてしまう場合は負閉路が存在する
                if self.dists[v]+d < self.dists[u]: return False
        return True

N, M, r = I()
G = BellmanFord(N,M)
G.add_edges(ind=0, bi=False)
if G.bellman_ford(r):
    for d in G.dists: print(d if d < INF else "INF")
else:
    print("NEGATIVE CYCLE")