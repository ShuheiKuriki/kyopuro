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
    def lower_bound(self,x):
        w = i = 0
        k = 1<<((self.n).bit_length())
        while k:
            if i+k <= self.n and w + self.bit[i+k] < x:
                w += self.bit[i+k]
                i += k
            k >>= 1
        return i+1

import sys; input = sys.stdin.readline
f = lambda:map(int,input().split())
def solve():
    N,M = f()
    A = list(f())
    S = sum(A)
    bits = [0,BIT(N),BIT(N),BIT(N)]
    for i,a in enumerate(A):bits[a].add(i+1,1)
    res = 0
    for _ in range(M):
        x,y,z = f()
        pre = A[x-1]
        S += y-pre
        A[x-1] = y
        bits[pre].add(x,-1)
        bits[y].add(x,1)
        lis1 = [bits[i].cumsum(z)for i in range(1,4)]
        lis2 = [bits[i].get_range_sum(z+1,N)for i in range(1,4)]
        if S%2:res-=1;continue
        half = S//2
        diff = half-sum((i+1)*l for i,l in enumerate(lis1))
        cnt = 0
        if diff > 0: # 増やしたい
            m = min(lis1[0],lis2[2])
            if m > 0:
                a = min(diff//2,m)
                lis1[2] += a; lis1[0] -= a
                lis2[2] -= a; lis2[0] += a
                diff -= a*2
                cnt += a
            m1 = min(lis1[0],lis2[1])
            m2 = min(lis1[1],lis2[2])
            if diff > m1+m2: cnt = -1
            else: cnt += diff
        elif diff < 0: # 減らしたい
            m = min(lis1[2],lis2[0])
            if m > 0:
                a = min((-diff)//2,m)
                lis1[0] += a; lis1[2] -= a
                lis2[0] -= a; lis2[2] += a
                diff += a*2
                cnt += a
            m1 = min(lis1[1],lis2[0])
            m2 = min(lis1[2],lis2[1])
            if -diff > m1+m2: cnt = -1
            else: cnt -= diff
        res += cnt
    return res
if __name__ == '__main__':
    print(*[f"Case #{t+1}: {solve()}"for t in range(int(*f()))],sep='\n')