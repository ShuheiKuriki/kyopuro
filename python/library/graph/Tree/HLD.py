"""
    HLD（重軽分解）
    verify: https://atcoder.jp/contests/abc294/tasks/abc294_g
"""
# 一点加算区間和取得
# Binary Indexed Tree (Fenwick Tree, 1-indexed)
class BIT:
    def __init__(self, n):
        self.n = n
        self.bit = [0]*(n+1)
        self.el = [0]*(n+1)
    def cumsum(self, i): # sum of [1,i]
        s = 0
        while i>0:
            s += self.bit[i]
            i -= i & -i
        return s
    def add(self, i, x):
        # assert i > 0
        self.el[i] += x
        while i<=self.n:
            self.bit[i] += x
            i += i & -i
    def get(self, i):return self.el[i]
    def get_range_sum(self, i, j):return self.cumsum(j)-self.cumsum(i-1)
    def set(self, i, x):
        # assert i > 0
        self.add(i, x-self.el[i])

from collections import*
class HLD:
    def __init__(self, N):
        self.V = N
        self.adj = [[]for _ in range(N)]
        self.edges = [0]*(N-1)
        self.parent = [-1]*N
        self.sub_size = [1]*N
        self.depth = [0]*N
        self.heavy_child = [-1]*N # 最も重い子の頂点
        self.head = list(range(N)) # その頂点が属するヘビーパスの先頭
        self.ord = [-1]*N # ヘビーパスを順に並べたときの各頂点の順序
        self.idx = 1 # BITに合わせて1-indexed
        self.bit = BIT(self.V)

    def add_edges(self, ind=1, bi=True):
        for i,(a,b,w) in enumerate(tuple(I()) for _ in range(self.V-1)):
            a-=ind; b-=ind
            self.adj[a].append(b)
            self.edges[i] = [a,b,w]
            if bi:self.adj[b].append(a)

    def add_edge(self, i, a, b, w, ind=1, bi=True):
        a-=ind; b-=ind
        self.adj[a].append(b)
        self.edges[i] = [a,b,w]
        if bi: self.adj[b].append(a)
        
    def update(self, i, w=-1):
        if w>=0:self.edges[i][2] = w
        u,v,w = self.edges[i]
        if self.depth[u]>self.depth[v]:v = u
        # 深い方の頂点に値を設定する
        self.bit.set(self.ord[v],w)

    def query(self, v, u):
        dist = 0
        while self.head[v]!=self.head[u]:
            # head[v]がhead[u]より遠くなるようにswap
            if self.depth[self.head[v]]<self.depth[self.head[u]]:v,u = u,v
            dist += self.bit.get_range_sum(self.ord[self.head[v]], self.ord[v])
            v = self.parent[self.head[v]]
        # vの方が深くなるようにswap
        if self.depth[u]>self.depth[v]:u,v = v,u
        dist += self.bit.get_range_sum(self.ord[u]+1, self.ord[v])
        return dist
        
    def build(self):        
        def _dfs1(start):
            """
                depthとsub_sizeとheavy_childを求める
            """
            stack = deque([start])
            order = [start]
            while stack:
                # 行きがけ(pre-order)
                v = stack.pop()
                for u in self.adj[v]:
                    if u==self.parent[v]: continue
                    self.parent[u]=v
                    stack.append(u); order.append(u)
                    self.depth[u] = self.depth[v]+1
            for v in order[::-1]:
                # 帰りがけ(post-order)
                for u in self.adj[v]:
                    if u==self.parent[v]: continue
                    self.sub_size[v] += self.sub_size[u]
                    if self.heavy_child[v]==-1 or self.sub_size[u]>self.sub_size[self.heavy_child[v]]:
                        self.heavy_child[v] = u
        def _dfs2(start):
            """
                headとordを求める
            """
            que = deque([start])
            while len(que):
                v = que.popleft()
                self.ord[v] = self.idx
                self.idx += 1
                for u in self.adj[v]:
                    if u==self.parent[v]:continue
                    elif u==self.heavy_child[v]:
                        self.head[u] = self.head[v]
                        que.appendleft(u)
                    else:
                        que.append(u)
        _dfs1(0);_dfs2(0)
        for i in range(self.V-1):self.update(i)

import sys;RL=sys.stdin.readline;I=lambda:map(int,RL().split())
G = HLD(int(*I()))
G.add_edges(ind=1,bi=True)
G.build()
ans=[]
for _ in range(int(*I())):
    t,a,b = I()
    if t==1:G.update(a-1,b)
    else:ans.append(G.query(a-1,b-1))
print(*ans,sep='\n')