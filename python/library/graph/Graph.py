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
    self.order = []
    self.fr = [0]*self.V

  def add_edges(self, ind=1, bi=True):
    for i in range(self.E):
      a,b = map(int, input().split())
      a -= ind; b -= ind
      self.edge[a].append(b)
      if bi: self.edge[b].append(a)

  def add_revs(self, ind=1, bi=True): #トポソ用
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

  def topo_sort(self): #topological sort
    updated = [0]*self.V
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
  def dp(self): #トポソしてから
    #記録したい値の配列を定義
    self.dp = [0]*self.V
    for v in self.order: #トポロジカル順序
      for u in self.edge[v]: #辺は逆向き
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
    return

  #O(ElogV),頂点数10**5以下
  def dijkstra_heap(self,s):
    self.dists = [float('inf')] * self.V; self.dists[s] = 0
    used = [False] * self.V; used[s] = True
    vlist = [] #vlist : [sからの暫定(未確定)最短距離,頂点]のリスト
    #edge[s] : sから出る枝の[重み,終点]のリスト
    for e in self.edge[s]: heapq.heappush(vlist,e) #sの隣の点は枝の重さがそのまま暫定最短距離となる
    while len(vlist):
      #まだ使われてない頂点の中から最小の距離のものを探す→確定させる
      d,v = heapq.heappop(vlist)
      #[d,v]:[sからの(確定)最短距離,頂点]
      if used[v]: continue
      self.dists[v] = d; used[v] = True
      for d,w in edge[v]:
        if not used[w]: heapq.heappush(vlist,[self.dists[v]+d,w])

  #O(ElogV),重みが整数の場合のみ
  def dijkstra_fast(self,s,mod):
    self.dists = [float('inf')] * self.V; self.dists[s] = 0 #始点sから各頂点への最短距離
    used = [False] * self.V; used[s] = True
    vlist = []
    #vlist : [sからの暫定(未確定)最短距離,頂点]のリスト
    #edge[s] : sから出る枝の[重み,終点]のリスト
    for w,v in self.edge[s]:
      heapq.heappush(vlist,w*mod+v) #sの隣の点は枝の重さがそのまま暫定最短距離となる
    while len(vlist):
      #まだ使われてない頂点の中から最小の距離のものを探す→確定させる
      #d, v : sからの(確定)最短距離, 頂点
      d,v = divmod(heapq.heappop(vlist),mod)
      if used[v]: continue
      self.dists[v] = d; used[v] = True
      for d,w in edge[v]:
        if not used[w]: heapq.heappush(vlist,(self.dists[v]+d)*mod+w)

N, M = map(int, input().split())
G = Graph(N,M)
G.add_edges(ind=1, bi=True)