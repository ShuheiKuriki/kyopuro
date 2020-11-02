import sys
input = sys.stdin.readline
#input = io.BytesIO(os.read(0,os.fstat(0).st_size)).readline
N = int(input())
parent = [0]*N
edge = [[] for _ in range(N)]
for i in range(N):
  A = list(map(int, input().split()))
  edge[i] = A[1:]
  for a in A[1:]:
    parent[a] = i
def bfs(start):
  stack = [start]
  depth = [0]*N
  while stack:
    v = stack.pop()
    for u in edge[v]:
      #頂点に対する処理
      depth[u] = depth[v] + 1
      stack.append(u)
  return depth
depth = bfs(0)
K = N.bit_length()
db = [[0]*N for _ in range(K)]
db[0] = parent[:]
for i in range(1,K):
  for j in range(N):
    db[i][j] = db[i-1][db[i-1][j]]
Q = int(input())
ans = [0]*Q
def go_up(v,x):
  p = 0
  while x:
    if x%2:
      v = db[p][v]
    p += 1
    x >>= 1
  return v
for i in range(Q):
  u,v = map(int, input().split())
  d = depth[u]-depth[v]
  if d>=0:
    u = go_up(u,d)
  else:
    v = go_up(v,-d)
  if u==v:
    ans[i] = u
    continue
  for p in range(K-1,-1,-1):
    if db[p][u]!=db[p][v]:
      u, v = db[p][u], db[p][v]
  ans[i] = parent[u]
print(*ans, sep='\n')
