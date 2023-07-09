"""
    オイラーツアー
    verify:https://atcoder.jp/contests/abc294/tasks/abc294_g
"""
import sys;RL=sys.stdin.readline;I=lambda:map(int,RL().split())
# 一点加算区間和取得
# Binary Indexed Tree (Fenwick Tree, 1-indexed)
class BIT:
    def __init__(self, n):
        self.n = n
        self.bit = [0]*(n+1)
        self.el = [0]*(n+1)
    def cumsum(self, i): # sum of [1,i]
        s = 0
        while i > 0:
            s += self.bit[i]
            i -= i & -i
        return s
    def add(self, i, x):
        # assert i > 0
        self.el[i] += x
        while i <= self.n:
            self.bit[i] += x
            i += i & -i
    def get(self, i): return self.el[i]
    def get_range_sum(self, i, j): return self.cumsum(j) - self.cumsum(i-1)
    def set(self, i, x):
        # assert i > 0
        self.add(i, x-self.el[i])
# 一点更新（更新方法は任意）区間取得（区間に比例しないモノイド作用素）
# https://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=DSL_2_A
class SegmentTree():
    def __init__(self, n, oper, e):
        self.n = n
        self.oper = oper
        self.e = e
        self.log = (n - 1).bit_length()
        self.size = 1 << self.log
        self.data = [e] * (2 * self.size)
        self.el = [e] * n

    def _update(self, k):
        self.data[k] = self.oper(self.data[2 * k], self.data[2 * k + 1])

    def build(self, arr):
        # assert len(arr) <= self.n
        self.el = arr[:]
        for i in range(self.n):
            self.data[self.size + i] = arr[i]
        for i in range(self.size-1,0,-1):
            self._update(i)

    def set(self, p, x):
        # assert 0 <= p < self.n
        self.el[p] = x
        p += self.size
        self.data[p] = x
        for i in range(self.log):
            p >>= 1
            self._update(p)

    def get(self, p):
        # assert 0 <= p < self.n
        return self.el[p]

    def prod(self, l, r):
        # 半開区間[l,r)
        # assert 0 <= l <= r <= self.n
        sml = smr = self.e
        l += self.size
        r += self.size
        while l < r:
            if l & 1:
                sml = self.oper(sml, self.data[l])
                l += 1
            if r & 1:
                r -= 1
                smr = self.oper(self.data[r], smr)
            l >>= 1
            r >>= 1
        return self.oper(sml, smr)

    def all_prod(self):
        return self.data[1]

from collections import*
class Tree:
    def __init__(self, N):
        self.V = N
        self.adj = [[]for _ in range(N)]
        self.edges = [0]*(N-1)
        self.parent = [-1]*N
        self.depth = [0]*N
        self.first_visit = [-1]*N
        self.last_visit = [-1]*N

    def add_edges(self, ind=1, bi=True):
        for i,(a,b,w) in enumerate(tuple(I()) for _ in range(self.V-1)):
            a-=ind; b-=ind
            self.adj[a].append((b,i))
            self.edges[i] = [a,b,w]
            if bi:self.adj[b].append((a,i))

    def add_edge(self, i, a, b, w, ind=1, bi=True):
        a-=ind; b-=ind
        self.adj[a].append((b,i))
        self.edges[i] = [a,b,w]
        if bi: self.adj[b].append((a,i))

    def euler_tour(self, start):
        edge_weight = [] # 頂点の重みを記録（出る時は負）
        tour = [] # (深さ,頂点)
        stack = deque([(start,-1,1)]) # (頂点, 辺のid, 1:入 or 0:出)
        tour_idx = 0
        while stack:
            # 行きがけ(pre-order)
            v,i0,t = stack.pop()
            w = self.edges[i0][2] if i0>=0 else 0
            if t==1:
                # 入るとき
                self.first_visit[v] = tour_idx
                edge_weight.append(w)
                tour.append((self.depth[v],v))
                stack.append((v,i0,0))
                for u,i1 in self.adj[v][::-1]:
                    if u==self.parent[v]: continue
                    self.parent[u]=v
                    stack.append((u,i1,1))
                    self.depth[u] = self.depth[v]+1
            else:
                # 出るとき
                self.last_visit[v] = tour_idx
                edge_weight.append(-w)
                p = self.parent[v]
                tour.append((self.depth[p],p)) # 親に戻す
            tour_idx += 1
        e = ((1<<31)-1,-1) #深さの最大値より大きければOK
        self.st = SegmentTree(tour_idx,min,e)
        self.st.build(tour)
        self.bit = BIT(tour_idx)
        for i,w in enumerate(edge_weight):self.bit.set(i+1,w)
        del tour,edge_weight

    def lca(self, v, u):
        f = min(self.first_visit[v], self.first_visit[u])
        l = max(self.last_visit[v], self.last_visit[u])
        return self.st.prod(f,l)[1] # (深さ,頂点)[1]

    def update(self, i, w):
        a,b,_ = self.edges[i]
        if self.depth[a] < self.depth[b]:a,b = b,a
        self.bit.set(self.first_visit[a]+1,w)
        self.bit.set(self.last_visit[a]+1,-w)

    def get_dist(self, v, u):
        l = self.lca(v,u)
        dv = self.bit.cumsum(self.first_visit[v]+1)
        du = self.bit.cumsum(self.first_visit[u]+1)
        dl = self.bit.cumsum(self.first_visit[l]+1)
        return dv+du-dl*2

N = int(*I())
G = Tree(N)
G.add_edges(ind=1, bi=True)
G.euler_tour(0)
ans = []
for _ in range(int(*I())):
    t,a,b = I()
    if t==1:
        G.update(a-1,b)
    else:
        ans.append(G.get_dist(a-1,b-1))
print(*ans,sep='\n')