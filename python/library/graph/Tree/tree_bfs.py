"""
BFS:verify
01-BFS:未verify
"""
import sys; input = sys.stdin.readline
I = lambda:map(int,input().split())
from collections import deque
INF = 10**18
class Tree:
    def __init__(self, N):
        self.V = N
        self.edge = [[] for _ in range(N)]

    def add_edges(self, ind=1, bi=True):
        for a,*A in [list(I()) for _ in range(self.V-1)]:
            a -= ind; b = A[0] - ind
            atob,btoa = (b,a) if len(A) == 1 else ((A[1],b),(A[1],a))
            self.edge[a].append(atob)
            if bi: self.edge[b].append(btoa)

    def add_edge(self, a, b, cost=None, ind=1, bi=True):
        a -= ind; b -= ind
        atob,btoa = (b,a) if cost is None else ((cost,b),(cost,a))
        self.edge[a].append(atob)
        if bi: self.edge[b].append(btoa)

    def bfs(self, s, g=-1, zero_one=False):
        """
        zero_one=Falseなら通常のBFS、Trueなら01-BFS
        """
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
                if zero_one:
                    if weight:
                        que.append(u)
                    else:
                        que.appendleft(u)
                else:
                    que.append(u)
        return -1

N = int(input())
G = Tree(N)
G.add_edges(ind=1, bi=True)
G.bfs(0, ind=0, zero_one=False)