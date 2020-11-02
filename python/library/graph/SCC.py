# 強連結成分分解(SCC): グラフGに対するSCCを行う
# 入力: <N>: 頂点サイズ, <G>: 順方向の有向グラフ, <RG>: 逆方向の有向グラフ
# 出力: (<ラベル数>, <各頂点のラベル番号>)

class SCC:
  def __init__(self, N, M):
    self.V = N
    self.E = M
    self.edge = [[] for _ in range(self.V)]
    self.edge_rev = [[] for _ in range(self.V)]
    self.v_to_g = [None]*self.V
    self.label = 0
  
  def add_edges(self, ind=1):
    for i in range(self.E):
      a,b = map(int, input().split())
      a -= ind; b -= ind
      self.edge[a].append(b)
      self.edge_rev[b].append(a)
  
  def add_edge(self, a, b):
    self.edge[a].append(b)
    self.edge_rev[b].append(a)
  
  def scc(self):
    order = []
    used = [0]*self.V
    def dfs(s):
      stack = [s]; used[s] = 1
      while stack:
        v = stack[-1]
        for u in self.edge[v]:
          if not used[u]:
            used[u] = 1; stack.append(u); break
        else:
          stack.pop(); order.append(v)
    def rdfs(s, col):
      stack = [s]; self.v_to_g[s] = col; used[s] = 1
      while stack:
        v = stack.pop()
        for u in self.edge_rev[v]:
          if not used[u]:
            self.v_to_g[u] = col; used[u] = 1; stack.append(u)
    for i in range(self.V):
      if not used[i]:
        dfs(i)
    used = [0]*self.V
    for s in order[::-1]:
      if not used[s]:
        rdfs(s, self.label); self.label += 1

  # 縮約後のグラフを構築
  def construct(self):
    G0 = [set() for i in range(self.label)]
    for v in range(self.V):
      lbs = self.v_to_g[v]
      for w in self.edge[v]:
        lbt = self.v_to_g[w]
        if lbs == lbt:
          continue
        G0[lbs].add(lbt)
    return G0

import sys
input = sys.stdin.readline
N, M = map(int, input().split())
G = SCC(N,M)
G.add_edges(0)
G.scc()
print(G.label)
ans = [[] for _ in range(G.label)]
for v in range(N):
  ans[G.v_to_g[v]].append(v)
for a in ans:
  print(len(a),*a)