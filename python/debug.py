def solve(n,A):
  p = 0
  if n%2==0:
    ans = 1
  else:
    ans = 0
  for i in range(n-1,-1,-2):
    if i==0:
      if p!=A[i]:
        ans ^= 1
        break
    elif p==0:
      if A[i]-A[i-1]!=A[i]^A[i-1]:
        ans ^= 1
        break
      p = A[i]-A[i-1]
    else:
      if p<A[i]:
        ans ^= 1
        break
      if (p-A[i])-A[i-1]!=(p-A[i])^A[i-1]:
        ans ^= 1
        break
      p = (p-A[i])-A[i-1]
  else:
    if p!=0:
      ans ^= 1
  if ans==1:
    ans = 'Second'
  else:
    ans = 'First'
  return ans

N = int(input())
from itertools import groupby, accumulate, product, permutations, combinations
for per in product(range(1,N+1),repeat=N):
  A = list(per)
  if solve(N,A)=='Second':
    print(A,solve(N,A))

