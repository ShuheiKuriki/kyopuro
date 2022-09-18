# 最小費用流(minimum cost flow) BellmanFord O(FEV)
class MinCostFlow:
  def __init__(self, n):
    self.n = n
    self.G = [[] for i in range(n)]

  def add_edge(self, f, t, cap, cost):
    # [to, cap, cost, rev]
    self.G[f].append([t, cap, 0, cost, len(self.G[t])])
    self.G[t].append([f, 0, 0, -cost, len(self.G[f])-1])

  def minCostFlow(self, s, t, flow):
    n = self.n
    G = self.G
    prevv = [0]*n; preve = [0]*n
    INF = 10**9+7

    res = 0
    while flow:
      dist = [INF]*n
      dist[s] = 0
      update = 1
      while update:
        update = 0
        for v in range(n):
          if dist[v] == INF:
            continue
          gv = G[v]
          for i in range(len(gv)):
            to, cap, flow, cost, rev = gv[i]
            if cap > 0 and dist[v] + cost < dist[to]:
              dist[to] = dist[v] + cost
              prevv[to] = v; preve[to] = i
              update = 1
      if dist[t] == INF:
        return -1

      d = flow; v = t
      while v != s:
        d = min(d, G[prevv[v]][preve[v]][1])
        v = prevv[v]
      flow -= d
      res += d * dist[t]
      v = t
      while v != s:
        e = G[prevv[v]][preve[v]]
        e[1] -= d
        if G[v][e[4]][2]==0:
          e[2] += d
        else:
          G[v][e[4]][2] -= d
        G[v][e[4]][1] += d
        v = prevv[v]
    return res

import sys; input = sys.stdin.readline
f = lambda:map(int,input().split())

n, m, flow = f()
graph = MinCostFlow(n)
for i in range(m):
  u, v, c, d = f()
  graph.add_edge(u, v, c, d)
print(graph.minCostFlow(0, n-1, flow))