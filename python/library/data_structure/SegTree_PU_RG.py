# 一点更新（更新方法は任意）区間取得（区間に比例しないモノイド作用素）
# https://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=DSL_2_A
class SegmentTree():
    def __init__(self, n, oper, e):
        self.n = n
        self.oper = oper
        self.e = e
        self.log = (n - 1).bit_length()
        self.size = 1 << self.log
        self.data = [e] * (2 * self.size)

    def update(self, k):
        self.data[k] = self.oper(self.data[2 * k], self.data[2 * k + 1])

    def build(self, arr):
        # assert len(arr) <= self.n
        for i in range(self.n):
            self.data[self.size + i] = arr[i]
        for i in range(self.size-1,0,-1):
            self.update(i)

    def set(self, p, x):
        # assert 0 <= p < self.n
        p += self.size
        self.data[p] = x
        for i in range(self.log):
            p >>= 1
            self.update(p)

    def get(self, p):
        # assert 0 <= p < self.n
        return self.data[p + self.size]

    def prod(self, l, r):
        # 半開区間[l,r)
        # assert 0 <= l <= r <= self.n
        sml = smr = self.e
        l += self.size
        r += self.size
        while l < r:
            if l & 1:
                sml = self.oper(sml, self.data[l])
                l += 1
            if r & 1:
                r -= 1
                smr = self.oper(self.data[r], smr)
            l >>= 1
            r >>= 1
        return self.oper(sml, smr)

    def all_prod(self):
        return self.data[1]

    def max_right(self, l, f):
        # assert 0 <= l <= self.n
        # assert f(self.)
        if l == self.n: return self.n
        l += self.size
        sm = self.e
        while True:
            while l % 2 == 0: l >>= 1
            if not f(self.oper(sm, self.data[l])):
                while l < self.size:
                    l = 2 * l
                    if f(self.oper(sm, self.data[l])):
                        sm = self.oper(sm, self.data[l])
                        l += 1
                return l - self.size
            sm = self.oper(sm, self.data[l])
            l += 1
            if (l & -l) == l: break
        return self.n

    def min_left(self, r, f):
        # assert 0 <= r <= self.n
        # assert f(self.)
        if r == 0: return 0
        r += self.size
        sm = self.e
        while True:
            r -= 1
            while r > 1 and (r % 2): r >>= 1
            if not f(self.oper(self.data[r], sm)):
                while r < self.size:
                    r = 2 * r + 1
                    if f(self.oper(self.data[r], sm)):
                        sm = self.oper(self.data[r], sm)
                        r -= 1
                return r + 1 - self.size
            sm = self.oper(self.data[r], sm)
            if (r & -r) == r: break
        return 0

import sys;RL=sys.stdin.readline;I=lambda:map(int,RL().split())

def op(x, y):
    return min(x,y)

e = (1<<31)-1

N, Q = I()
A = [e for _ in range(N)]

st = SegmentTree(N,op,e)
st.build(A)

ans = []
for i in range(Q):
    t,*B = I()
    if t == 0:
        x,y = B
        st.set(x,y)
    else:
        x,y = B
        ans.append(st.prod(x,y+1))
print(*ans, sep='\n')