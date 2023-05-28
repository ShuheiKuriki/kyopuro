# ポテンシャル（重み）付きUnionFind（非零閉路有りの場合にも対応）
# verify：https://atcoder.jp/contests/abc280/tasks/abc280_f
class UnionFind():
    def __init__(self, n):
        self.n = n
        self.parents = [-1] * n
        self.weight = [0] * n
        self.add = lambda a,b: INF if INF in [a,b] else a+b # INFの場合を考慮した重み加算

    def find(self, x):
        if self.parents[x] < 0: return x,self.weight[x]
        # 経路圧縮
        self.parents[x],w = self.find(self.parents[x])
        self.weight[x] = self.add(self.weight[x], w)
        return self.parents[x],self.weight[x]
    
    def union(self, x, y, w):
        (rx,wx),(ry,wy) = self.find(x),self.find(y)
        if rx == ry:
            # xとyが既に同グループの場合
            if self.add(wx, w) != wy:
                # 元々のポテンシャル差と新たな重みが異なる場合、非零閉路になる
                self.weight[rx] = INF
        else:
            # xとyをグループ結合する場合
            if self.parents[rx] > self.parents[ry]:
                # マージテクを効かせるため、x側を要素数が大きいグループにする
                rx,ry,wx,wy,w = ry,rx,wy,wx,-w
            self.parents[rx] += self.parents[ry]
            self.parents[ry] = rx
            if max(wx,wy) == INF:
                # どちらかが非零閉路なら、結合後のグループも非零閉路になる
                self.weight[rx] = INF
            else:
                self.weight[ry] += (wx + w) - wy

    def same(self, x, y):
        return self.find(x)[0] == self.find(y)[0]

    def roots(self):
        return [i for i, x in enumerate(self.parents) if x < 0]

    def members(self, x):
        root = self.find(x)[0]
        return [i for i in range(self.n) if self.find(i)[0] == root]

    def size(self,x):
        return abs(self.parents[self.find(x)[0]])

    def groups(self):
        roots = [i for i, x in enumerate(self.parents) if x < 0]
        r_to_g = {r:i for i,r in enumerate(roots)}
        groups = [[]for _ in roots]
        for i in range(self.n):groups[r_to_g[self.find(i)[0]]].append(i)
        return groups

import sys;RL=sys.stdin.readline;I=lambda:map(int,RL().split())
INF = 10**18
N,M,Q = I()
uf = UnionFind(N)