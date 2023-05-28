"""
    LCA（最小共通祖先）ライブラリ
    verify: https://atcoder.jp/contests/abc014/tasks/abc014_4
"""
import sys;RL=sys.stdin.readline;I=lambda:map(int,RL().split())
from collections import*
class LCA:
    def __init__(self, N):
        self.edge = [[] for _ in range(N)]
        self.parent = [-1]*N
        self.N = N
        self.K = N.bit_length()

    def add_edges(self, ind=1, bi=False):
        for a,b in [tuple(I()) for _ in range(self.N-1)]:
            a -= ind; b -= ind
            self.edge[a].append(b)
            self.parent[b] = a
            if bi: self.edge[b].append(a)

    def add_edge(self, a, b, ind=1, bi=False):
        a -= ind; b -= ind
        self.edge[a].append(b)
        self.parent[b] = a
        if bi: self.edge[b].append(a)

    def doubling(self, root):
        self.depth = [-1]*N
        self.db = [[0]*N for _ in range(self.K)]
        que = deque([root])
        self.depth[root] = 0
        while que:
            v = que.popleft()
            for u in self.edge[v]:
                if self.depth[u]>=0:continue
                self.depth[u] = self.depth[v] + 1
                self.parent[u] = v
                que.append(u)
        self.db[0] = self.parent[:]
        for i in range(1,self.K):
            for j in range(N):
                self.db[i][j] = self.db[i-1][self.db[i-1][j]]

    def go_up(self, v, x):
        p = 0
        while x:
            if x % 2:
                v = self.db[p][v]
            p += 1
            x >>= 1
        return v

    def lca(self, u, v):
        d = self.depth[u]-self.depth[v]
        if d >= 0:
            u = self.go_up(u,d)
        else:
            v = self.go_up(v,-d)
        if u == v: return u
        for p in range(self.K-1,-1,-1):
            if self.db[p][u] != self.db[p][v]:
                u, v = self.db[p][u], self.db[p][v]
        return self.parent[u]

N = int(*I())
G = LCA(N)
G.add_edges(ind=1, bi=True)
G.doubling(0)
def solve(a,b):
    r = G.lca(a-1,b-1)
    return G.depth[a-1]+G.depth[b-1]-G.depth[r]*2+1
print(*[solve(*I())for _ in range(int(*I()))],sep='\n')