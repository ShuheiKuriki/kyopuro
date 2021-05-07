N, Q = map(int, input().split())
# N: 処理する区間の長さ 0_indexed
class SegmentTree:
    def __init__(self,N):
        self.N0 = 2**(N-1).bit_length()
        self.INF = 2**31-1
        self.data = [self.INF]*(2*self.N0)
    # a_k の値を x に更新
    def update(self, k, x):
        k += self.N0-1
        self.data[k] = x
        while k >= 0:
            k = (k - 1) // 2
            self.data[k] = min(self.data[2*k+1], self.data[2*k+2])
    # 区間[l, r)の最小値
    def query(self, l, r):
        L = l + self.N0; R = r + self.N0
        s = self.INF
        while L < R:
            if R & 1:
                R -= 1
                s = min(s, self.data[R-1])

            if L & 1:
                s = min(s, self.data[L-1])
                L += 1
            L >>= 1; R >>= 1
        return s

import sys
input = sys.stdin.readline

ans = []
seg = SegmentTree(N)
for i in range(Q):
    com,x,y = map(int, input().split())
    if com==0:
        seg.update(x,y)
    else:
        ans.append(seg.query(x,y+1))
print(*ans, sep='\n')