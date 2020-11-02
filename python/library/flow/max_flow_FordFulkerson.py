# Ford-Fulkerson algorithm O(F|E|)
class FordFulkerson:
  def __init__(self, N):
    self.N = N
    self.edge = [[] for i in range(N)]

  def add_edge(self, fr, to, cap):
    forward = [to, cap, 0, None]
    forward[3] = backward = [fr, 0, 0, forward]
    self.edge[fr].append(forward)
    self.edge[to].append(backward)

  def add_multi_edge(self, v1, v2, cap1, cap2):
    edge1 = [v2, cap1, 0, None]
    edge1[3] = edge2 = [v1, cap2, 0, edge1]
    self.edge[v1].append(edge1)
    self.edge[v2].append(edge2)

  def dfs(self, v, t, f):
    if v == t:
      return f
    used = self.used
    used[v] = 1
    for e in self.edge[v]:
      w, cap, flow, rev = e
      if cap and not used[w]:
        d = self.dfs(w, t, min(f, cap))
        if d:
          e[1] -= d
          if rev[2]==0:
            e[2] += d
          else:
            rev[2] -= d
          rev[1] += d
          return d
    return 0

  def flow(self, s, t):
    flow = 0
    f = INF = 10**9 + 7
    N = self.N
    while f:
      self.used = [0]*N
      f = self.dfs(s, t, INF)
      flow += f
    return flow

import sys
readline = sys.stdin.readline
sys.setrecursionlimit(10**6)

N, M = map(int, readline().split())
ff = FordFulkerson(N)
for i in range(M):
  u, v, c = map(int, readline().split())
  ff.add_edge(u, v, c)
ans = ff.flow(0, N-1)
print(ans)