"""
二部グラフ判定（非連結対応）: https://atcoder.jp/contests/abc282/tasks/abc282_d
"""
import sys; input = sys.stdin.readline
I = lambda:map(int,input().split())
from collections import*
INF = 10**18
class Bipartite:
    def __init__(self, N, M=-1):
        self.V = N
        if M >= 0: self.E = M
        self.edge = [[] for _ in range(self.V)]

    def add_edges(self, ind=1, bi=False):
        for a,*A in [tuple(I()) for _ in range(self.E)]:
            a -= ind; b = A[0] - ind
            atob,btoa = (b,a) if len(A) == 1 else ((A[1],b),(A[1],a))
            self.edge[a].append(atob)
            if bi: self.edge[b].append(btoa)

    def add_edge(self, a, b, cost=None, ind=1, bi=False):
        a -= ind; b -= ind
        atob,btoa = (b,a) if cost is None else ((cost,b),(cost,a))
        self.edge[a].append(atob)
        if bi: self.edge[b].append(btoa)

    def is_bipartite(self):
        """
        グラフ全体が二部グラフか判定する（非連結の場合も考慮）
        """
        self.colors = [INF]*self.V
        base_color = 0
        for start in range(self.V):
            if G.colors[start] < INF: continue
            #step1(初期化)
            que = deque([start])
            # self.colors = defaultdict(lambda: INF)
            self.colors[start] = base_color
            #step2(ループ)
            while len(que):
                #step2-1(queから頂点を出す)
                v = que.popleft()
                #step2-3(隣接頂点をループ)
                for u in self.edge[v]:
                    #step2-3-1(隣接頂点の色を計算)
                    ncolor = self.colors[v] ^ 1
                    #step2-3-2(隣接頂点の色が既に決まっていた場合の処理)
                    if self.colors[u] < INF:
                        if ncolor != self.colors[u]: return False
                        continue
                    #step2-3-3(colors配列にncolorをset)
                    self.colors[u] = ncolor
                    #step2-3-4(queに隣接頂点を入れる)
                    que.append(u)
            base_color += 2
        return True

N,M = I()
G = Bipartite(N,M)
G.add_edges(ind=1,bi=True)
# G.is_bipartite()
print(sum(v*(N-v)for v in Counter(G.colors).values())//2-M if G.is_bipartite() else 0)