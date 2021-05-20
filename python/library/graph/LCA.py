import sys
input = sys.stdin.readline
from collections import deque
class Tree:
  def __init__(self, N):
    self.V = N
    self.edge = [deque([]) for _ in range(N)]
    self.order = []
  
  def add_edges(self, ind=1, bi=True):
    for i in range(self.V-1):
      a,b = map(int, input().split())
      a -= ind; b -= ind
      self.edge[a].append(b)
      if bi: self.edge[b].append(a)

  def add_edge(self, a, b, bi=True):
    self.edge[a].append(b)
    if bi: self.edge[b].append(a)

  def dfs(self, start):
    stack = deque([start])
    self.parent = [self.V]*self.V; self.parent[start] = start
    self.order.append(start)
    self.depth = [0]*self.V
    while stack:
      v = stack[-1]
      while len(self.edge[v]):
        u = self.edge[v].popleft()
        if u==self.parent[v]: continue
        self.depth[u] = self.depth[v] + 1
        self.parent[u]=v
        stack.append(u); self.order.append(u)
        break
      else:
        stack.pop()
  
  def set_db(self):
    self.K = self.V.bit_length()
    self.db = [[0]*self.V for _ in range(self.K)]
    self.db[0] = self.parent[:]
    for i in range(self.K-1):
      for j in range(self.V):
        self.db[i+1][j] = self.db[i][self.db[i][j]]
  
  def lca(self, u, v):
    def go_up(v,x):
      p = 0
      while x:
        if x%2:
          v = self.db[p][v]
        p += 1
        x >>= 1
      return v
    diff = self.depth[u]-self.depth[v]
    # res = abs(diff)
    if diff>=0:
      u = go_up(u,diff)
    else:
      v = go_up(v,-diff)
    if u==v:
      return u
    for p in range(self.K-1,-1,-1):
      if self.db[p][u]!=self.db[p][v]:
        u, v = self.db[p][u], self.db[p][v]
        # res += 1<<(p+1)
    return self.parent[u] # res+2

N = int(input())
G = Tree(N)
G.add_edges(ind=1, bi=True)
G.dfs(0)
G.set_db()