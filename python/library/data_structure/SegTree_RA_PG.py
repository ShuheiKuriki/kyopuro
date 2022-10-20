# 区間更新（可換モノイド作用素）一点取得
# https://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=DSL_2_D
class SegmentTree():
    def __init__(self, n, mapping, id):
        self.n = n
        self.id = id
        self.log = (n - 1).bit_length()
        self.size = 1 << self.log
        self.data = [self.id] * (2 * self.size)
        self.mapping = mapping
    
    def get(self, p):
        # assert 0 <= p < self.n
        res = self.id
        p += self.size
        for _ in range(self.log+1):
            res = self.mapping(res, self.data[p])
            p >>= 1
        return res

    def set(self, p, x):
        # assert 0 <= p < self.n
        p += self.size
        self.data[p] = x

    def build(self, arr):
        # assert len(arr) <= self.n
        for i in range(self.n):
            self.data[self.size + i] = arr[i]

    def range_apply(self, l, r, x):
        # 半開区間[l,r)
        # assert 0 <= l <= r <= self.n
        l += self.size
        r += self.size
        while l < r:
            if l & 1:
                self.data[l] = self.mapping(self.data[l], x)
                l += 1
            if r & 1:
                r -= 1
                self.data[r] = self.mapping(self.data[r], x)
            l >>= 1
            r >>= 1

import sys; input = sys.stdin.readline
I = lambda:map(int,input().split())

N, Q = I()
# 可換作用素のみ可
def mapping(a,b): return a+b
id = 0
st = SegmentTree(N+1,mapping,id)

ans = []
for _ in range(Q):
    t,*X = I()
    if t==0:
        l,r,x = X
        st.range_apply(l,r+1,x)
    else:
        i, = X
        ans.append(st.get(i))
print(*ans, sep='\n')