class UnionFind():
    def __init__(self, n):
        self.n = n
        self.parents = [-1] * n
        self.roots = set()
        self.minh = [i//W for i in range(n)]
        self.minw = [i%W for i in range(n)]
        self.maxh = [i//W for i in range(n)]
        self.maxw = [i%W for i in range(n)]

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
        self.minh[x] = min(self.minh[x], self.minh[y])
        self.maxh[x] = max(self.maxh[x], self.maxh[y])
        self.minw[x] = min(self.minw[x], self.minw[y])
        self.maxw[x] = max(self.maxw[x], self.maxw[y])
        self.roots.discard(y)

    def same(self, x, y):
        return self.find(x) == self.find(y)

import sys; input = sys.stdin.readline
I = lambda:map(int,input().split())

H,W = I()
from collections import *
dic = defaultdict(lambda:set())
T = [tuple(I()) for _ in range(H)]
for h in range(H):
    for w,a in enumerate(T[h]): dic[a].add(h*W+w)
uf = UnionFind(H*W)
lis = sorted(dic.keys())
dh = [-1,0,1,0]
dw = [0,-1,0,1]
ans = 0
for height1,height2 in zip(lis,lis[1:]):
    uf.roots |= dic[height1]
    for hw in dic[height1]:
        h,w = divmod(hw,W)
        for i in range(4):
            nh,nw = h+dh[i],w+dw[i]
            if not(0<=nh<H and 0<=nw<W):continue
            if T[nh][nw] <= height1:
                uf.union(hw,nh*W+nw)
    sub = set()
    for r in uf.roots:
        rh,rw = divmod(r,W)
        if uf.minh[r]==0 or uf.maxh[r]==H-1 or uf.minw[r]==0 or uf.maxw[r]==W-1:
            sub.add(r)
            continue
        ans += (height2-height1)*abs(uf.parents[r])
    for s in sub:uf.roots.discard(s)
print(ans)