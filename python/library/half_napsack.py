import sys
input = sys.stdin.readline
N, Wlim = map(int, input().split())
n1 = N//2
n2 = N-n1
V1,V2,W1,W2 = [0]*n1,[0]*n2,[0]*n1,[0]*n2
for i in range(n1):
  V1[i],W1[i] = map(int, input().split())
for i in range(n2):
  V2[i],W2[i] = map(int, input().split())
from collections import defaultdict
from bisect import *
def make(V,W,n):
  res = {0}
  dic = defaultdict(lambda: 0)
  for i in range(n):
    lis = sorted(res,reverse=True)
    for l in lis:
      res.add(l+W[i])
      dic[l+W[i]] = max(dic[l+W[i]],dic[l]+V[i])
  res = sorted(res)
  for i in range(1,len(res)):
    dic[res[i]] = max(dic[res[i]], dic[res[i-1]])
  return res, dic
res1,dic1 = make(V1,W1,n1)
res2,dic2 = make(V2,W2,n2)
ans = 0
for r1 in res1:
  if r1>Wlim:
    break
  r2 = res2[bisect_right(res2,Wlim-r1)-1]
  ans = max(ans, dic1[r1]+dic2[r2])
print(ans)