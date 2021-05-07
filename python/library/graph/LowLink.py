import sys
input = sys.stdin.readline
from collections import deque
class LowLink:
    def __init__(self, N, M):
        self.V = N
        self.E = M
        self.edge = [[] for _ in range(self.V)]
        self.edges = [0]*M
        self.visited = [False]*N
        self.parent = [N]*N
        self.order = [N]*N
        self.low = [N]*N
    
    def add_edges(self, ind=1):
        for i in range(self.E):
            a,b = map(int, input().split())
            a -= ind
            b -= ind
            self.edge[a].append(b)
            self.edge[b].append(a)
            self.edges[i] = (a,b)

    def add_edge(self, a, b):
        self.edge[a].append(b)
        self.edge[b].append(a)

    def low_link(self, start):
        self.start = start
        stack = deque([start])
        self.parent[start] = -1
        self.order[start] = 0
        self.cnts = [0]*self.V
        order = 1
        while stack:
            v = stack[-1]
            for u in self.edge[v]:
                if u==self.parent[v]:
                    continue
                if self.order[u] < self.order[v]: #後退辺の処理
                    self.low[v] = min(self.low[v], self.order[u])
                elif self.cnts[u] == 0: #行きがけ
                    self.order[u] = self.low[u] = order
                    self.parent[u] = v
                    stack.append(u)
                    self.cnts[u] += 1
                    order += 1
                    break
                elif self.cnts[u] == 1: #帰りがけ
                    self.low[v] = min(self.low[v], self.low[u])
                    self.cnts[u] += 1
            else:
                stack.pop() #帰り
        return
    
    def bridge(self):
        res = []
        for a,b in self.edges:
            if G.order[a] > G.order[b]:
                a,b = b,a
            if G.low[b] > G.order[a]:
                res.append((a,b))
        return res

    def cycle(self):
        res = [0]*self.V
        for a,b in self.edges:
            if G.order[a] > G.order[b]:
                a,b = b,a
            if G.low[b] <= G.order[a]:
                res[a] = 1; res[b] = 1
        return res
    
    def articulation(self):
        res = []
        for v in range(self.V):
            cnt = 0
            for u in self.edge[v]:
                if self.parent[v] == u or self.parent[u] != v:
                    continue
                if self.order[v] <= self.low[u]:
                    cnt += 1
            if v == self.start:
                if cnt >= 2:
                res.append(v)
            elif cnt >= 1:
                res.append(v)
        return res


N, M = map(int, input().split())
G = LowLink(N, M)
G.add_edges(0)
G.low_link(0)
ans = G.articulation()
if len(ans):
    print(*ans, sep='\n')