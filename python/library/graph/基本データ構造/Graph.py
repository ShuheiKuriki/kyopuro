import sys
input = sys.stdin.readline
# sys.setrecursionlimit(10**6)
from collections import deque
from heapq import *
INF = float('inf')
class Graph:
    def __init__(self, N, M=-1):
        self.V = N
        if M>=0: self.E = M
        self.edge = [[] for _ in range(self.V)]
        self.edge_rev = [[] for _ in range(self.V)]
        self.order = []
        self.to = [0]*self.V
        self.visited = [False]*self.V
        self.dp = [0]*self.V

    def add_edges(self, ind=1, cost=False, bi=False, rev=False):
        for i in range(self.E):
            if cost:
                a,b,d = map(int, input().split())
                a -= ind; b -= ind
                self.edge[a].append((d,b))
                if rev: self.edge_rev[b].append((d,a))
                if not bi: self.to[b] += 1
                if bi: self.edge[b].append((d,a))
            else:
                a,b = map(int, input().split())
                a -= ind; b -= ind
                self.edge[a].append(b)
                if rev: self.edge_rev[b].append(a)
                if not bi: self.to[b] += 1
                if bi: self.edge[b].append(a)

    def add_edge(self, a, b, cost=-1, bi=False, rev=False):
        if cost>=0:
            self.edge[a].append((cost, b))
            if rev: self.edge_rev[b].append((cost, a))
            if bi: self.edge[b].append((cost, a))
        else:
            self.edge[a].append(b)
            if rev: self.edge_rev[b].append(a)
            if bi: self.edge[b].append(a)
        if not bi: self.to[b] += 1

    def dfs_rec(self, v):
        if self.visited[v]: return self.dp[v]
        self.visited[v] = True
        for u in self.edge[v]:
            self.dp[v] += self.dfs_rec(u)
        return self.dp[v]
    
    def dfs(self, s):
        que = deque([(-1,s)])
        visited = [False]*self.V
        while len(que):
            w,v = que.pop()
            if visited[v]: continue
            if w>=0:
                self.dp[w] += self.dp[v]
            visited[v] = True
            for u in self.edge[v]:
                que.append((v,u))

    def topo_sort(self): #topological sort
        updated = [0]*self.V
        for start in range(self.V):
            if self.to[start] or updated[start]: continue
            que = deque([start])
            while que:
                v = que.popleft()
                self.order.append(v)
                updated[v] = 1
                for u in self.edge[v]:
                    self.to[u] -= 1
                    if self.to[u]: continue
                    que.append(u)
    def dp(self): #トポソしてから
        # self.dp = [0]*self.V
        #行きがけ
        for v in self.order:
            #配るDP
            for u in self.edge[v]:
                self.dp[u] = max(self.dp[u], self.dp[v]+1)
        #帰りがけ
        for v in self.order[::-1]:
            #配るDP
            for u in self.edge_rev[v]:
                self.dp[u] = max(self.dp[u], self.dp[v]+1)

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

    def bellman_ford(self, s):
        dist = [INF]*self.V
        dist[s] = 0
        for _ in range(self.V):
            for v in range(self.V):
                for d,u in self.edge[v]:
                    dist[u] = min(dist[u], dist[v]+d)
        for v in range(self.V):
            for d,u in self.edge[v]:
                if dist[u] > dist[v]+d: return -1


N, M = map(int, input().split())
G = Graph(N,M)
G.add_edges(ind=1, cost=False, bi=False, rev=False)
