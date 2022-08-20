"""
デバッグ用、木をランダム生成
"""
import sys
input = sys.stdin.readline
from collections import deque
INF = 10**10

class UnionFind():
    def __init__(self, n):
        self.n = n
        self.parents = [-1] * n

    def find(self, x):
        if self.parents[x] < 0: return x
        # 経路圧縮
        self.parents[x] = self.find(self.parents[x])
        return self.parents[x]

    def union(self, x, y):
        x = self.find(x); y = self.find(y)
        if x == y: return
        # マージテク
        if self.parents[x] > self.parents[y]: x,y = y,x
        self.parents[x] += self.parents[y]
        self.parents[y] = x

    def same(self, x, y):
        return self.find(x) == self.find(y)

class Tree:
    def __init__(self, N):
        self.V = N
        self.edge = [[] for _ in range(N)]
        self.edges = []

    def add_edge(self, a, b, cost=None, ind=0, bi=True):
        a -= ind; b -= ind
        atob,btoa = (b,a) if cost is None else ((cost,b),(cost,a))
        self.edge[a].append(atob)
        self.edges.append((a,b))
        if bi: self.edge[b].append(btoa)

    def bfs(self, s, g=-1, std=True):
        """
        std=Trueなら通常のBFS、std=Falseなら01-BFS
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
                if std or weight: que.append(u)
                else: que.appendleft(u)
        # 木であれば必ず到達するはず
        raise AssertionError

def solve(N):
    ans = N
    return ans

from random import *
T = int(input())
M = int(input())
for t in range(1,T+1):
    N = randint(3,M)
    G = Tree(N)
    uf = UnionFind(N)
    cnt = 0
    while cnt < N-1:
        u,v = sample(range(N),2)
        if uf.same(u,v): continue
        uf.union(u,v)
        G.add_edge(u,v)
        cnt += 1
    ac = G.bfs(0,1)
    res = solve(N)
    if ac != res:
        print("t:",t,"N:",N,"ac:",ac," res:",res)
        print(G.edges)
        print()