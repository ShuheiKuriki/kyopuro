class UnionFind():
    def __init__(self, n):
        self.n = n
        self.parents = [-1] * n
        self.dp = [-1] * n
        self.cnt = [0] * n

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

    def roots(self):
        return [i for i, x in enumerate(self.parents) if x < 0]

    def groups(self):
        roots = self.roots()
        r_to_g = {}
        for i, r in enumerate(roots):
            r_to_g[r] = i
        groups = [[] for _ in roots]
        for i in range(self.n):
            groups[r_to_g[self.find(i)]].append(i)
        return groups

import sys; input = sys.stdin.readline
I = lambda:map(int,input().split())

N,M = I()
uf = UnionFind(N)
for _ in range(M):
    s = input()[:-2].split()
    v,u,p = int(s[0])-1,int(s[2])-1,s[5]=='liar'
    if v==u:
        if p==1:
            exit(print(-1))
    elif uf.dp[v]==-1:
        if uf.dp[u]==-1:
            uf.dp[u]=False
        uf.dp[v]=uf.dp[u]^p
    else:
        if uf.dp[u]==-1:
            uf.dp[u]=uf.dp[v]^p
        elif uf.dp[v]^uf.dp[u]!=p:
            exit(print(-1))
    if not uf.same(v,u):
        uf.union(v,u)
        uf.cnt[v] += 1
ans = 1
for g in uf.groups():
    cnts = sum(uf.cnt[v]for v in g)
    ans += max(0,len(g)-cnts)
print(ans)