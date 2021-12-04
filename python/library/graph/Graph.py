import sys
input = sys.stdin.readline
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
        if self.visited[v]:
            return self.dp[v]
        for u in self.edge[v]:
            self.dp[v] += self.dfs_rec(u, v)
        self.visited[v] = True
        return self.dp[v]

    def topo_sort(self): #topological sort
        updated = [0]*self.V
        for start in range(self.V):
            if self.to[start] or updated[start]: continue
            stack = deque([start])
            while stack:
                v = stack.popleft()
                self.order.append(v)
                updated[v] = 1
                for u in self.edge[v]:
                    self.to[u] -= 1
                    if self.to[u]: continue
                    stack.append(u)
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
  
    def bfs(self, start):
        que = deque([start])
        self.min_cost = [-1]*self.V; self.min_cost[start]=0
        while len(que)>0:
            v = que.popleft()
            for u in self.edge[v]:
                if self.min_cost[u] == -1:
                    self.min_cost[u] = self.min_cost[u]+1
                    que.append(u)

    def bfs01(self, start):
        que = deque([start])
        self.min_cost = [-1]*self.V; self.min_cost[start]=0
        while len(que)>0:
            v = que.popleft()
            for weight, u in self.edge[v]:
                new_cost = self.min_cost[v] + weight
                if new_cost < self.min_cost[u]:
                    self.min_cost[u] = new_cost
                    if weight == 0: que.appendleft(u)
                    else: que.append(u)

    #O(ElogV)
    def dijkstra_heap(self, s):
        self.dists = [INF] * self.V
        self.dists[s] = 0
        que = [(0,s)] #que : [sからの暫定(未確定)最短距離,頂点]のリスト
        while len(que):
            cost, v = heappop(que)
            if self.dists[v] < cost: continue
            #[d,v]:[sからの(確定)最短距離,頂点]
            for weight, u in self.edge[v]:
                new_cost = self.dists[v]+weight
                if new_cost < self.dists[u]:
                    self.dists[u] = new_cost
                    heappush(que,(new_cost,u))

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
