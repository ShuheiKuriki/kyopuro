import sys
input = sys.stdin.readline
from collections import deque
class Tree:
  def __init__(self, N):
    self.V = N
    self.edge = [[] for _ in range(N)]
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

  def merge(self, a, b): return a+b
  
  def op(self,a): return a

  def dp(self, start):
    stack = deque([start])
    self.parent = [self.V]*self.V; self.parent[start] = -1
    self.order.append(start)
    #記録したい値の配列を定義
    self.ans = [1]*self.V
    while stack:
      v = stack.pop()
      for u in self.edge[v]:
        if u==self.parent[v]: continue
        self.parent[u]=v
        stack.append(u); self.order.append(u)
    for v in self.order[::-1]:
      for u in self.edge[v]:
        if u==self.parent[v]: continue
        self.ans[v] = self.merge(self.ans[v], self.op(self.ans[u])) #帰りがけ処理
  
  def rerooting(self, start):
    p_value = [0]*self.V #親側の値
    for v in self.order:
      cumL = [1]*(len(self.edge[v])+1)
      cumR = [1]*(len(self.edge[v])+1)
      for i,u in enumerate(self.edge[v]):
        if u==self.parent[v]:
          cumL[i+1] = self.merge(cumL[i], self.op(p_value[v]))
        else:
          cumL[i+1] = self.merge(cumL[i], self.op(self.ans[u]))
      for i,u in enumerate(self.edge[v][::-1]):
        if u==self.parent[v]:
          cumR[-i-2] = self.merge(cumR[-i-1], self.op(p_value[v]))
        else:
          cumR[-i-2] = self.merge(cumR[-i-1], self.op(self.ans[u]))
      for i,u in enumerate(self.edge[v]):
        if u==self.parent[v]: continue
        p_value[u] = self.merge(cumL[i], cumR[i+1])
        self.ans[u] = self.merge(self.ans[u], self.op(p_value[u]))
  
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

N = int(input())
G = Tree(N)
G.add_edges(ind=1, bi=True)
