import sys
input = sys.stdin.readline
from collections import deque
class Tree:
  def __init__(self, N):
    self.V = N
    self.edge = [[] for _ in range(N)]
    self.visited = [False]*N
    self.parent = [N]*N
  
  def add_edges(self, ind=1):
    for i in range(self.V-1):
      a,b = map(int, input().split())
      a -= ind; b -= ind
      self.edge[a].append(b)

  def add_edge(self, a, b):
    self.edge[a].append(b)
    self.edge[b].append(a)

  def dfs(self, start):
    stack = deque([start])
    self.parent[start] = -1
    self.cnts = [0]*self.V
    #記録したい値の配列を定義
    while stack:
      v = stack[-1]
      for u in self.edge[v]:
        if u==self.parent[v]:
          continue
        if self.cnts[u]==0: #行きがけ
          self.parent[u]=v
          stack.append(u)
          self.cnts[u] += 1
          break
        elif self.cnts[u]==1:
          self.cnts[u] += 1
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
    d.append((start,0))
    while len(d)>0:
      v,cnt = d.popleft()
      for w in self.edge[v]:
        if self.visited[w]==False:
          self.visited[w]=True
          d.append((w,cnt+1))
    return cnt