import sys
input = sys.stdin.readline
from collections import deque
sys.setrecursionlimit(10**5)
class Graph:
    def __init__(self, N, M=-1):
        self.V = N
        if M>=0: self.E = M
        self.edge = [[] for _ in range(self.V)]
        self.edge_rev = [[] for _ in range(self.V)]
        self.order = []
        self.to = [0]*self.V
        self.visited = [False]*self.V
        self.dp = [0]*self.V

    def add_edge(self, a, b, cost=-1, bi=False, rev=False):
        if cost>=0:
            self.edge[a].append((cost, b))
            if rev: self.edge_rev[b].append((cost, a))
            if bi: self.edge[b].append((cost, a))
        else:
            self.edge[a].append(b)
            if rev: self.edge_rev[b].append(a)
            if bi: self.edge[b].append(a)
        if not bi: self.to[b] += 1

    def dfs(self, dir, v):
        for d,u in self.edge[v]:
            if d != dir: continue
            if self.visited[u]: continue
            route.append((d,u))
            self.visited[u] = True
            self.dfs(d, u)
        for d,u in self.edge[v]:
            if self.visited[u]: continue
            route.append((d,u))
            self.visited[u] = True
            self.dfs(d, u)
        if dir!=-1:
            route.append(((dir+2)%4, v))
        return

N = 20
sh, sw = map(int, input().split())
start = sh*N + sw
G = Graph(N*N)
for i in range(N):
    for j,a in enumerate(input()):
        if a=="0":
            u = i*N+j
            G.add_edge(u, u+1, cost=3)
            G.add_edge(u+1, u, cost=1)
for i in range(N-1):
    for j,a in enumerate(input()):
        if a=="0":
            u = i*N+j
            G.add_edge(u, u+N, cost=2)
            G.add_edge(u+N, u, cost=0)
route = []
G.dfs(-1, start)
ans = ""
now = 0
cleared = set()
for d,v in route:
    ans += "L"*((d-now)%4)
    ans += "F"
    cleared.add(v)
    now = d
    if len(cleared)==N*N: break
from itertools import groupby
comp = groupby(ans)
res = ""
for k,v in comp:
    num = len(list(v))
    if num > 1: res += str(num)
    res += k
print(res)