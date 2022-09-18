# 区間更新（純粋な更新のみ、maxで更新を代用）一点取得
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
        #assert 0 <= p < self.n
        res = self.id
        p += self.size
        for _ in range(self.log+1):
            res = self.mapping(res, self.data[p])
            p >>= 1
        return res

    def set(self, p, x):
        #assert 0 <= p < self.n
        p += self.size
        self.data[p] = x

    def build(self, arr):
        #assert len(arr) <= self.n
        for i in range(self.n):
            self.data[self.size + i] = arr[i]

    def range_apply(self, l, r, x):
        #assert 0 <= l <= r <= self.n
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
f = lambda:map(int,input().split())

N, Q = f()
mapping = max
id = (-1,(1<<31)-1)
st = SegmentTree(N,mapping,id)

ans = []
for q in range(Q):
    t,*y = f()
    if t==0:
        s,t,x = y
        st.range_apply(s,t+1,(q,x))
    else:
        i, = y
        ans.append(st.get(i)[1])
print(*ans, sep='\n')