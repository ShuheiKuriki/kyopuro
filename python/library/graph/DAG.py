import sys
input = sys.stdin.readline
sys.setrecursionlimit(10**7)
from collections import deque
class Graph:
  def __init__(self, N, M=False):
    self.V = N
    if M: self.E = M
    self.edge = [[] for _ in range(self.V)]
    self.order = []
    self.fr = [0]*self.V

  def add_edges(self, ind=1, bi=True):
    for i in range(self.E):
      a,b = map(int, input().split())
      a -= ind; b -= ind
      self.edge[a].append(b)
      if bi: self.edge[b].append(a)

  def add_revs(self, ind=1, bi=True):
    for i in range(self.E):
      a,b = map(int, input().split())
      a -= ind; b -= ind
      self.edge[b].append(a)
      self.fr[a] += 1
      if bi: self.edge[b].append(a)

  def add_edge(self, a, b, bi=True):
    self.edge[a].append(b)
    if bi: self.edge[b].append(a)

  def dfs_rec(self, v, parent):
    if self.sth[v]>0: return self.sth[v]
    for u in self.edge[v]:
      if u==parent: continue
      self.sth[v] += self.dfs_rec(u, v)
    return self.sth[v]

  def dp(self): #topology → DP
    updated = [0]*self.V
    # topology
    for start in range(self.V):
      if self.fr[start] or updated[start]: continue
      stack = deque([start])
      while stack:
        v = stack.popleft()
        self.order.append(v)
        updated[v] = 1
        for u in self.edge[v]:
          self.fr[u] -= 1
          if self.fr[u]: continue
          stack.append(u)
    #記録したい値の配列を定義
    for v in self.order:
      for u in self.edge[v]:
        pass
        #　DPの遷移
  
  def bfs(self, start):
    d = deque([start])
    self.min_cost = [-1]*self.V; self.min_cost[start]=0
    while len(d)>0:
      v = d.popleft()
      for w in self.edge[v]:
        if self.min_cost[w]==-1:
          self.min_cost[w]=self.min_cost[v]+1
          d.append(w)
    return

N, M = map(int, input().split())
G = Graph(N,M)
G.add_edges(ind=1, bi=True)