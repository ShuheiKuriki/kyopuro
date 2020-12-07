# Dijkstra O(FElog(V))
from heapq import heappush, heappop
class MinCostFlow:
  INF = 10**18

  def __init__(self, N):
    self.N = N
    self.G = [[] for i in range(N)]

  def add_edge(self, fr, to, cap, cost):
    forward = [to, cap, 0, cost, None]
    backward = forward[4] = [fr, 0, 0, -cost, forward]
    self.G[fr].append(forward)
    self.G[to].append(backward)

  def minCostFlow(self, s, t, f):
    N = self.N; G = self.G
    INF = MinCostFlow.INF

    res = 0
    H = [0]*N
    prv_v = [0]*N
    prv_e = [None]*N

    d0 = [INF]*N
    dist = [INF]*N

    while f:
      dist[:] = d0
      dist[s] = 0
      que = [(0, s)]

      while que:
        c, v = heappop(que)
        if dist[v] < c:
          continue
        r0 = dist[v] + H[v]
        for e in G[v]:
          w, cap, _, cost, _ = e
          if cap > 0 and r0 + cost - H[w] < dist[w]:
            dist[w] = r = r0 + cost - H[w]
            prv_v[w] = v; prv_e[w] = e
            heappush(que, (r, w))
      if dist[t] == INF:
        return -1

      for i in range(N):
        H[i] += dist[i]

      d = f; v = t
      while v != s:
        d = min(d, prv_e[v][1])
        v = prv_v[v]
      f -= d
      res += d * H[t]
      v = t
      while v != s:
        e = prv_e[v]
        e[1] -= d
        if e[4][2]==0:
          e[2] += d
        else:
          e[4][2] -= d
        e[4][1] += d
        v = prv_v[v]
    return res

import sys,os,io
input = sys.stdin.readline
#input = io.BytesIO(os.read(0,os.fstat(0).st_size)).readline
n, m, f = map(int, input().split())
graph = MinCostFlow(n)
for i in range(m):
  u, v, c, d = map(int, input().split())
  graph.add_edge(u, v, c, d)
print(graph.minCostFlow(0, n-1, f))