import sys
input = sys.stdin.readline
sys.setrecursionlimit(10**7)
from collections import deque
import heapq
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

  def add_edges(self, ind=1, cost=False, bi=False, rev=False):
    for i in range(self.E):
      if cost:
        a,b,d = map(int, input().split())
        a -= ind; b -= ind
        self.edge[a].append((d,b))
        if rev: self.edge_rev[b].append((d,a))
        if not bi: self.to[b] += 1
        if bi: self.edge[b].append((d,a))
      else:
        a,b = map(int, input().split())
        a -= ind; b -= ind
        self.edge[a].append(b)
        if rev: self.edge_rev[b].append(a)
        if not bi: self.to[b] += 1
        if bi: self.edge[b].append(a)

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

  def dfs_rec(self, v):
    if self.visited[v]: return self.dp[v]
    for u in self.edge[v]:
      self.dp[v] += self.dfs_rec(u, v)
    self.visited[v] = True
    return self.dp[v]

  def topo_sort(self): #topological sort
    updated = [0]*self.V
    for start in range(self.V):
      if self.to[start] or updated[start]: continue
      stack = deque([start])
      while stack:
        v = stack.popleft()
        self.order.append(v)
        updated[v] = 1
        for u in self.edge[v]:
          self.to[u] -= 1
          if self.to[u]: continue
          stack.append(u)
  def dp(self): #トポソしてから
    # self.dp = [0]*self.V
    for v in self.order: #行きがけ
      for u in self.edge[v]:
        self.dp[u] = max(self.dp[u], self.dp[v]+1) #配るDP
    for v in self.order[::-1]: #帰りがけ
      for u in self.edge_rev[v]:
        self.dp[u] = max(self.dp[u], self.dp[v]+1) #配るDP
  
  def bfs(self, start):
    d = deque([start])
    self.min_cost = [-1]*self.V; self.min_cost[start]=0
    while len(d)>0:
      v = d.popleft()
      for w in self.edge[v]:
        if self.min_cost[w]==-1:
          self.min_cost[w]=self.min_cost[v]+1
          d.append(w)

  #O(ElogV)
  def dijkstra_heap(self,s):
    self.dists = [float('inf')] * self.V
    self.dists[s] = 0
    que = [(0,s)] #que : [sからの暫定(未確定)最短距離,頂点]のリスト
    while len(que):
      d,v = heapq.heappop(que)
      #[d,v]:[sからの(確定)最短距離,頂点]
      if self.dists[v]!=d: continue
      for d,w in self.edge[v]:
        new_d = self.dists[v]+d
        if new_d<self.dists[w]:
          self.dists[w] = new_d
          heapq.heappush(que,(new_d,w))

N, M, r = map(int, input().split())
G = Graph(N,M)
G.add_edges(ind=1, cost=False, bi=False, rev=False)

