import sys
input = sys.stdin.readline
from collections import deque
from heapq import *
# sys.setrecursionlimit(10**6)
INF = float('inf')
class Tree:
    def __init__(self, N):
        self.V = N
        self.edge = [[] for _ in range(N)]
        self.order = []
    
    def add_edges(self, ind=1, bi=True, cost=False):
        for _ in range(self.V-1):
            if cost:
                a,b,c = map(int, input().split())
                a -= ind; b -= ind
                self.edge[a].append((c,b))
                if bi: self.edge[b].append((c,a))
            else:
                a,b = map(int, input().split())
                a -= ind; b -= ind
                self.edge[a].append(b)
                if bi: self.edge[b].append(a)

    def add_edge(self, a, b, cost=None, bi=True):
        if cost is not None:
            self.edge[a].append((cost,b))
            if bi: self.edge[b].append((cost,a))
        else:
            self.edge[a].append(b)
            if bi: self.edge[b].append(a)

    def dp(self, start):
        stack = deque([start])
        self.parent = [self.V]*self.V; self.parent[start] = -1
        self.order.append(start)
        #記録したい値の配列を定義
        self.dp = [1]*self.V
        while stack:
            v = stack.pop()
            for u in self.edge[v]:
                if u==self.parent[v]: continue
                self.parent[u]=v
                stack.append(u); self.order.append(u)
        for v in self.order[::-1]:
            for u in self.edge[v]:
                if u==self.parent[v]: continue
                self.dp[v] += self.dp[u] #帰りがけ処理
    
    def bfs(self, s, g=-1, std=True): #01BFSならstd=False
        #step1(初期化)
        que = deque([s])
        self.dists = [INF]*self.V; self.dists[s]=0
        #step2(ループ)
        while len(que):
            #step2-1(queから頂点を出す)
            v = que.popleft()
            #step2-2(vがgと一致していたらgの最短距離が確定)
            if v==g: return self.dists[v]
            #step2-3(隣接頂点をループ)
            for u in self.edge[v]:
                #step2-3-1(ndistを計算)
                weight = 1
                ndist = self.dists[v] + weight
                #step2-3-2(ndist>=dists配列値なら意味がないのでスキップ)
                if ndist >= self.dists[u]: continue
                #step2-3-3(dists配列にndistをset)
                self.dists[u] = ndist
                #step2-3-4(queに隣接頂点を入れる)
                if std or weight: que.append(u)
                else: que.appendleft(u)
        return -1
    
    #O(ElogV)
    def dijkstra_heap(self, s, g=-1):
        #step1(初期化)
        que = [(0,s)] #que:[sからの暫定最短距離,頂点]のリスト
        self.dists = [INF]*self.V; self.dists[s] = 0
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
        return -1

N = int(input())
G = Tree(N)
G.add_edges(ind=1, bi=True)
