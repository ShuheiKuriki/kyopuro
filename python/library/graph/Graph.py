import sys
input = sys.stdin.readline
from collections import deque
class Graph:
  def __init__(self, N, M):
    self.V = N
    self.E = M
    self.edge = [[] for _ in range(self.V)]
    self.visited = [False]*self.V
    self.parent = [N]*self.V
  
  def add_edges(self, ind=1, bi=True):
    for i in range(self.E):
      a,b = map(int, input().split())
      a -= ind; b -= ind
      self.edge[a].append(b)
      if bi:
        self.edge[b].append(a)

  def add_edge(self, a, b, bi=True):
    self.edge[a].append(b)
    if bi:
      self.edge[b].append(a)

  def dfs(self, start):
    stack = deque([start])
    self.parent[start] = -1
    #記録したい値の配列を定義
    while stack:
      v = stack[-1]
      for u in self.edge[v]:
        if u==self.parent[v]:
          continue
        if self.parent[u]==N: #行きがけ
          self.parent[u]=v
          stack.append(u)
          break
        else:
          pass
          #帰りがけ処理
      else:
        stack.pop() #帰りがけまとめ
        if v==start:
          #根の帰りがけまとめ処理
          continue
        #根以外の帰りがけまとめ処理
    return
  
  def bfs(self, start):
    d = deque()
    self.visited[start]=True
    d.append((start, 0))
    while len(d)>0:
      v,cnt = d.popleft()
      for w in self.edge[v]:
        if self.visited[w]==False:
          self.visited[w]=True
          d.append((w,cnt+1))
    return cnt

N, M = map(int, input().split())
G = Graph(N,M)
G.add_edges(ind=1, bi=True)