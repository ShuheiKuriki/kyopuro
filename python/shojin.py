N, M = map(int, input().split())
w = list(map(int, input().split()))
A = [list(map(int, input().split())) for _ in range(M)]
A.sort(key=lambda x:(x[1], -x[0]))
maximum = 0
lis = [0]
dic = {0:0}
for l, v in A:
  if l>maximum:
    maximum = l
    lis.append(v)
    dic[v] = l
if lis[1]<max(w):
  print(-1)
  exit()
from itertools import groupby, accumulate, product, permutations, combinations
from bisect import *
ans = float('inf')
for perm in permutations(range(N),N):
  cum = [0]
  for p in perm:
    cum.append(cum[-1]+w[p])
  min_pos = [0]*N
  for i in range(1,N):
    for j in range(i):
      W = cum[i+1]-cum[j]
      dif = dic[lis[bisect_left(lis,W)-1]]
      min_pos[i] = max(min_pos[i], min_pos[j]+dif)
  ans = min(ans, min_pos[-1])
print(ans)
