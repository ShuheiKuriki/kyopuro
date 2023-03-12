# 区間加算区間和取得(RSQ and RAQ)
# Binary Indexed Tree (Fenwick Tree)
# verify https://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=DSL_2_G
class BIT:
    def __init__(self, n):
        self.n = n
        self.data = [0]*(n+1)
        self.el = [0]*(n+1)
    def sum(self, i):
        s = 0
        while i > 0:
            s += self.data[i]
            i -= i & -i
        return s
    def add(self, i, x):
        # assert i > 0
        self.el[i] += x
        while i <= self.n:
            self.data[i] += x
            i += i & -i
    def get(self, i, j=None):
        if j is None:
            return self.el[i]
        return self.sum(j) - self.sum(i-1)

import sys; input = sys.stdin.readline
I = lambda:map(int,input().split())

def solve():
    ans = []
    N, Q = I()
    data0 = BIT(N+1)
    data1 = BIT(N+1)
    for _ in range(Q):
        p,*y = I()
        if p==0:
            l,r,x = y
            data0.add(l,-x*(l-1))
            data0.add(r+1,x*r)
            data1.add(l,x)
            data1.add(r+1,-x)
        else:
            s,t = y
            ans.append(data1.sum(t)*t+data0.sum(t)-data1.sum(s-1)*(s-1)-data0.sum(s-1))
    return ans
print(*solve(),sep='\n')

