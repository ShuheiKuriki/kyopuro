import sys;RL=sys.stdin.readline;I=lambda:map(int,RL().split())
# sys.setrecursionlimit(10**6)
from collections import*
from heapq import*
INF = 10**18
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

    def dp_dfs_rec(self, v):
        if self.visited[v]: return self.dp[v]
        self.visited[v] = True
        for u in self.edge[v]:
            # 行きがけ
            self.dp[u] += self.dp[v]
            # 帰りがけ
            self.dp[v] += self.dp_dfs_rec(u)
        return self.dp[v]

    def dp_dfs(self, s):
        # 根が分かっている場合
        que = deque([(-1,s)])
        visited = [False]*self.V
        while len(que):
            p,v = que.pop()
            if visited[v]: continue
            if p >= 0:
                # 帰りがけ（post_order）
                self.dp[p] += self.dp[v]
            visited[v] = True
            for c in self.edge[v]:
                que.append((v,c))

    def topo_sort(self):
        # トポロジカルソート
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
    def dfs_dp(self):
        # 根が分かっていない場合、トポソしてorderを定めてからdpする
        self.topo_sort()
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

    def bfs(self, s, g=-1, zero_one=False):
        """
        zero_one=Falseなら通常のBFS、Trueなら01-BFS
        """
        #step1(初期化)
        que = deque([s])
        self.dists = [INF]*self.V
        # self.dists = defaultdict(lambda: INF)
        self.dists[s]=0
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
                if zero_one:
                    if weight:
                        que.append(u)
                    else:
                        que.appendleft(u)
                else:
                    que.append(u)
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

    def bellmanford(self, s):
        dist = [INF]*self.V
        dist[s] = 0
        for _ in range(self.V):
            for v in range(self.V):
                for d,u in self.edge[v]:
                    dist[u] = min(dist[u], dist[v]+d)
        for v in range(self.V):
            for d,u in self.edge[v]:
                if dist[u] > dist[v]+d: return -1


N, M = I()
G = Graph(N,M)
G.add_edges(ind=1, bi=False)
