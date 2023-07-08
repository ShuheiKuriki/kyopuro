"""
ダイクストラ法:単一始点最短経路問題、非負辺、計算量O(ElogV)
"""
import sys; input = sys.stdin.readline
I = lambda:map(int,input().split())
from heapq import *
INF = 10**9
# errprint = lambda x:print(x,file=sys.stderr)
class Graph:
    def __init__(self, N, M=-1):
        self.V = N
        if M>=0: self.E = M
        self.edge = [set()for _ in range(self.V)]

    def add_edge(self, a, b, cost=None, ind=1, bi=False):
        a -= ind; b -= ind
        atob,btoa = (b,a) if cost is None else ((cost,b),(cost,a))
        self.edge[a].add(atob)
        if bi: self.edge[b].add(btoa)

    def delete_edge(self, a, b, cost=None, ind=1, bi=False):
        a -= ind; b -= ind
        atob,btoa = (b,a) if cost is None else ((cost,b),(cost,a))
        self.edge[a].discard(atob)
        if bi: self.edge[b].discard(btoa)

    def dijkstra_heap(self, s):
        #step1(初期化)
        que = [(0,s)] #que:[sからの暫定最短距離,頂点]のリスト
        dists = [INF]*self.V
        dists[s] = 0
        #step2(ループ)
        while len(que):
            #step2-1(queから最短距離と頂点を出す)
            dist, v = heappop(que)
            #step2-1-1(dist>dists[v]なら古い情報なのでスキップ)
            if dist > dists[v]: continue
            #step2-3(隣接頂点をループ)
            for weight, u in self.edge[v]:
                #step2-3-1(ndistを計算)
                ndist = dists[v] + weight
                #step2-3-2(ndist>=dists配列値なら意味がないのでスキップ)
                if ndist >= dists[u]: continue
                #step2-3-3(dists配列にndistをset)
                dists[u] = ndist
                #step2-3-4(queに(ndist,隣接頂点)を入れる)
                heappush(que,(ndist,u))
        return sum(dists)

import sys;RL=sys.stdin.readline
I=lambda:map(int,RL().split())
from random import*
N,M,D,K = I()
A = [tuple([i]+list(I()))for i in range(M)]
shuffle(A)
Gs = [Graph(N,M)for _ in range(D)]
for d in range(D):
    for _,u,v,w in A:
        Gs[d].add_edge(u,v,cost=w,ind=1,bi=True)
ans = [0]*M
cnt_list = [(0,d)for d in range(D)]
for i,u,v,w in A:
    scores = []
    t = (11500001+M*M/2)/(M*M) if M*M > 4000000 else 11500001/(M*M)
    T = int(t)
    T += random()<t-T
    if T > 1:
        for j in range(min(T, len(cnt_list))):
            cnt, d = cnt_list[j]
            pre_score = Gs[d].dijkstra_heap(u-1)
            Gs[d].delete_edge(u,v,cost=w,ind=1,bi=True)
            aft_score = Gs[d].dijkstra_heap(u-1)
            scores.append((aft_score - pre_score, d))
            Gs[d].add_edge(u,v,cost=w,ind=1,bi=True)
        min_day = min(scores)[1]
    else:
        min_day = cnt_list[0][1]
    Gs[min_day].delete_edge(u,v,cost=w,ind=1,bi=True)
    ans[i] = min_day+1
    cnt_list = sorted((c+(d==min_day),d) for c,d in cnt_list if c+(d==min_day) < K)
    # errprint(f"min_day:{min_day+1}")
print(*ans)
# errprint("")