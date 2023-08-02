# verify:https://atcoder.jp/contests/abc289/tasks/abc289_g
from collections import deque
class Line():
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __call__(self, x):
        return self.a * x + self.b

class ConvexHullTrick():
    '''
        追加する直線の傾きが単調、かつクエリのx座標が単調なケース
        min用, O(N+Q)
    '''  
    def __init__(self):
        self.deq = deque()

    def _check_unnecessity(self, l1: Line, l2: Line, l3: Line):
        return (l2.a-l1.a)*(l3.b-l2.b) >= (l2.b-l1.b)*(l3.a-l2.a)
    
    def add_line(self, line: Line):
        # add f_i(x)=a*x+b
        while len(self.deq) >= 2 and self._check_unnecessity(self.deq[-2], self.deq[-1], line):
            self.deq.pop()
        self.deq.append(line)
    
    def query(self, x):
        # return min{i} f_i(x)
        while len(self.deq) >= 2 and self.deq[0](x) >= self.deq[1](x):
            self.deq.popleft()
        return self.deq[0](x)

import sys;RL=sys.stdin.readline;I=lambda:map(int,RL().split())
N,M = I()
B = sorted(I())[::-1]

CHT = ConvexHullTrick()
for i in range(1,N+1):
    CHT.add_line(Line(-i,-B[i-1]*i)) # minに変換するため-1倍する
 
ans = [0]*M
for i,c in sorted(enumerate(I()),key=lambda x:x[1]):
    ans[i] = -CHT.query(c)
print(*ans)