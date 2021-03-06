import sys
input = sys.stdin.readline
N, T = map(int, input().split())
A = list(map(int, input().split()))
n1 = N//2
n2 = N-n1
A1 = A[:n1]
A2 = A[n1:]
from itertools import groupby, accumulate, product, permutations, combinations
def make(m,B):
  res = set()
  for pro in product([0,1], repeat = m):
    cnt = 0
    for i in range(m):
      if pro[i]==1:
        cnt += B[i]
    res.add(cnt)
  res = sorted(list(res))
  return res
from bisect import *
lis1 = make(n1,A1)
lis2 = make(n2,A2)
ans = 0
for r1 in lis1:
  if r1>T:
    break
  r2 = lis2[bisect_right(lis2,T-r1)-1]
  ans = max(ans, r1+r2)
print(ans)