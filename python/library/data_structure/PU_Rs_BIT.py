# 一点更新（更新方法は任意）区間和取得
# Binary Indexed Tree (Fenwick Tree, 1-indexed)
class BIT:
    def __init__(self, n):
        self.n = n
        self.bit = [0]*(n+1)
        self.el = [0]*(n+1)
    def sum(self, i): # sum of [1,i]
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
    def get(self, i, j=None):
        if j is None:
            return self.el[i]
        return self.sum(j) - self.sum(i-1)
    def lower_bound(self,x):
        w = i = 0
        k = 1<<((self.n).bit_length())
        while k:
            if i+k <= self.n and w + self.bit[i+k] < x:
                w += self.bit[i+k]
                i += k
            k >>= 1
        return i+1