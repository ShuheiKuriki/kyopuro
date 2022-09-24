# 強連結成分分解(SCC）
# upsolve: https://atcoder.jp/contests/practice2/tasks/practice2_g
from collections import deque
class SCC:
    def __init__(self, N, M=0):
        self.V = N
        self.E = M
        self.edge = [[] for _ in range(self.V)]
        self.edge_que = [deque([]) for _ in range(self.V)]
        self.edge_rev = [[] for _ in range(self.V)]
        self.v_to_g = [None]*self.V
    
    def add_edges(self, ind=1):
        for _ in range(self.E):
            a,b = f()
            a -= ind; b -= ind
            self.edge_que[a].append(b)
            self.edge_rev[b].append(a)
        self.edge = [list(es) for es in self.edge_que]

    def add_edge(self, a, b):
        self.edge[a].append(b)
        self.edge_que[a].append(b)
        self.edge_rev[b].append(a)
    
    def scc(self):
        order = []
        used = [False]*self.V
        def dfs(s):
            used[s] = True; stack = [s]
            while stack:
                v = stack[-1]
                while len(self.edge_que[v]):
                    u = self.edge_que[v].popleft()
                    if used[u]: continue
                    used[u] = True; stack.append(u)
                    break
                else:
                    stack.pop(); order.append(v)
        def rdfs(s, gnum):
            used[s] = True; stack = [s]
            self.v_to_g[s] = gnum
            while stack:
                v = stack.pop()
                for u in self.edge_rev[v]:
                    if used[u]: continue
                    self.v_to_g[u] = gnum
                    used[u] = True; stack.append(u)
        for s in range(self.V):
            if used[s]: continue
            dfs(s)
        used = [0]*self.V
        self.gnum = 0
        for s in order[::-1]:
            if used[s]: continue
            rdfs(s, self.gnum)
            self.gnum += 1

        self.groups = [[] for _ in range(self.gnum)]
        for v in range(self.V):
            gv = self.v_to_g[v]
            self.groups[gv].append(v)

    def constrcut(self):
        # 縮約後のグラフgroupEdgeを構築、トポロジカルソートされる
        self.groupEdge = [set() for _ in range(self.gnum)]
        for v in range(self.V):
            gv = self.v_to_g[v]
            for u in self.edge[v]:
                gu = self.v_to_g[u]
                if gv == gu: continue
                self.groupEdge[gv].add(gu)

import sys; input = sys.stdin.readline
f = lambda:map(int,input().split())
N, M = f()
G = SCC(N,M)
G.add_edges(ind=0)
G.scc()
print(G.gnum)
for g in G.groups: print(len(g),*g)