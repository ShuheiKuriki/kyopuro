N = int(input())
A = [[0]*N for _ in range(3)]
A[0] = list(map(int, input().split()))
B = [[0]*N for _ in range(3)]
C = [int(input()) for _ in range(N-1)]
B[0][0] = A[0][0]
for i in range(1,N):
  B[0][i] = C[i-1]
if N>=2:
  A[1][0] = B[0][1]
  B[1][0] = A[0][1]
if N>=3:
  A[2][0] = B[0][2]
  B[2][0] = A[0][2]
def mex(a,b):
  lis = [0]*3
  lis[a] += 1
  lis[b] += 1
  for i in range(3):
    if lis[i]==0:
      return i
for i in range(1,3):
  for j in range(1,N):
    A[i][j] = mex(A[i-1][j], A[i][j-1])
for i in range(1,3):
  for j in range(1,N):
    B[i][j] = mex(B[i-1][j], B[i][j-1])
from collections import defaultdict
d = defaultdict(lambda: 0)
for i in range(min(N,3)):
  for j in range(N):
    d[A[i][j]] += 1
for i in range(min(N,3)):
  for j in range(N):
    d[B[i][j]] += 1
for i in range(min(N,3)):
  for j in range(min(N,3)):
    d[A[i][j]] -= 1
if N>=4:
  d[0] += (N-3)**2//2
  d[1] += (N-3)**2//2
  if N%2==0:
    if A[2][3]!=0 and B[2][3]!=0:
      d[0] += 1
    else:
      d[1] += 1
print(d[0],d[1],d[2])



