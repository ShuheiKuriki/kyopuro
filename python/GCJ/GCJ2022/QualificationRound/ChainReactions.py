import sys
input = sys.stdin.readline
from collections import deque
sys.setrecursionlimit(10**6)
class Tree:
    def __init__(self, N, F):
        self.V = N
        self.edge = [[] for _ in range(N)]
        self.order = []
        self.repr = F[:]
        self.total = F[:]
    
    def add_edges(self, ind=1, bi=True, cost=False):
        for _ in range(self.V-1):
            if cost:
                a,b,c = map(int, input().split())
                a -= ind; b -= ind
                self.edge[a].append((c,b))
                if bi: self.edge[b].append((c,a))
            else:
                a,b = map(int, input().split())
                a -= ind; b -= ind
                self.edge[a].append(b)
                if bi: self.edge[b].append(a)

    def add_edge(self, a, b, cost=None, bi=True):
        if cost is not None:
            self.edge[a].append((cost,b))
            if bi: self.edge[b].append((cost,a))
        else:
            self.edge[a].append(b)
            if bi: self.edge[b].append(a)

    def dfs(self, start):
        stack = deque([start])
        self.parent = [self.V]*self.V; self.parent[start] = -1
        self.order.append(start)
        while stack:
            v = stack.pop()
            for u in self.edge[v]:
                if u==self.parent[v]: continue
                self.parent[u]=v
                stack.append(u); self.order.append(u)
        for v in self.order[::-1]:
            lis = []
            for u in self.edge[v]:
                if u==self.parent[v]: continue
                self.total[v] += self.total[u] #帰りがけ処理
                lis.append(self.repr[u])
            if len(lis) > 0:
                self.total[v] -= min(lis + [self.repr[v]])
                if self.repr[v] < min(lis):
                    self.repr[v] = min(lis)

T = int(input())
ans = [0]*T
for t in range(T):
    N = int(input())
    F = list(map(int, input().split()))
    P = list(map(int, input().split()))
    G = Tree(N+1,[0]+F)
    for i in range(N):
        G.add_edge(P[i],i+1,bi=False)
    G.dfs(0)
    ans[t] = f"Case #{t+1}: {G.total[0]}"
print(*ans, sep='\n')