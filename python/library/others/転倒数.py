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

# 転倒数を求める
def get_inversion(N,A):
    bit = BIT(N)
    cnt = 0
    for i in range(N):
        cnt += bit.get_range_sum(A[i],N)
        bit.add(A[i],1)
    return cnt

import sys;I=lambda:map(int,sys.stdin.readline().split())
N = int(*I())
A = list(I())
print(get_inversion(N,A))