"""
ダイクストラ法:単一始点最短経路問題、非負辺、計算量O(ElogV)
"""
import sys; input = sys.stdin.readline
I = lambda:map(int,input().split())
from heapq import *
INF = 10**18
class Graph:
    def __init__(self, N, M=-1):
        self.V = N
        if M>=0: self.E = M
        self.edge = [[] for _ in range(self.V)]
        # self.edge_dic = {}

    def add_edges(self, ind=1, bi=False):
        for a,*A in [tuple(I()) for _ in range(self.E)]:
            a -= ind; b = A[0] - ind
            atob,btoa = (b,a) if len(A) == 1 else ((A[1],b),(A[1],a))
            self.edge[a].append(atob)
            # self.edge_dic[(a,b)] = i
            if bi:
                self.edge[b].append(btoa)
                # self.edge_dic[(b,a)] = i

    def add_edge(self, a, b, cost=None, ind=1, bi=False):
        a -= ind; b -= ind
        atob,btoa = (b,a) if cost is None else ((cost,b),(cost,a))
        self.edge[a].append(atob)
        if bi: self.edge[b].append(btoa)

    def dijkstra_heap(self, s, g=-1):
        #step1(初期化)
        que = [(0,s)] #que:[sからの暫定最短距離,頂点]のリスト
        self.dists = [INF]*self.V; self.dists[s] = 0
        self.prev = [-1]*self.V
        #step2(ループ)
        while len(que):
            #step2-1(queから最短距離と頂点を出す)
            dist, v = heappop(que)
            #step2-1-1(dist>dists[v]なら古い情報なのでスキップ)
            if dist > self.dists[v]: continue
            #step2-2(vがgと一致していたらgの最短距離が確定)
            if v==g: return self.dists[v]
            #step2-3(隣接頂点をループ)
            for weight, u in self.edge[v]:
                #step2-3-1(ndistを計算)
                ndist = self.dists[v] + weight
                #step2-3-2(ndist>=dists配列値なら意味がないのでスキップ)
                if ndist >= self.dists[u]: continue
                #step2-3-3(dists配列にndistをset)
                self.dists[u] = ndist
                #step2-3-4(queに(ndist,隣接頂点)を入れる)
                heappush(que,(ndist,u))
                self.prev[u] = v
        return -1

N, M = I()
G = Graph(N,M)
G.add_edges(ind=1, bi=True)
G.dijkstra_heap(s=0)

# 頂点の場合
ans = [N]
now = N-1
while now != 0:
    now = G.prev[now]
    ans.append(now+1)
print(*ans[::-1])

# 辺の場合
# ans = []
# now = N-1
# while now != 0:
#     pre = G.prev[now]
#     ans.append(G.edge_dic[(pre,now)])
#     now = pre
# print(*ans[::-1])