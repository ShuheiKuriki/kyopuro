# Binary Indexed Tree (Fenwick Tree)
class BIT_max:
    def __init__(self, n):
        self.n = n
        self.bit = [0]*(n+1)
        self.el = [0]*(n+1)
    def query(self, i):
        s = 0
        while i > 0:
            s = max(s,self.bit[i])
            i -= i & -i
        return s
    def update(self, i, x):
        # assert i > 0
        self.el[i] = max(self.el[i],x)
        while i <= self.n:
            self.bit[i] = max(self.bit[i],x)
            i += i & -i