import sys; input = sys.stdin.readline
I = lambda:map(int,input().split())
N = int(*I())
A = [list(I()) for _ in range(N)]
A.sort()

# 正なら反時計回り、負なら時計回り
def cross(a, b, c):
  return (b[0]-a[0])*(c[1]-a[1]) - (b[1]-a[1])*(c[0]-a[0])

# 上側凸包
stack1 = [A[0],A[1]]
i = 2
while len(stack1)>=2 and i<=N-1:
  if cross(stack1[-2], stack1[-1], A[i]) >= 0:
    stack1.pop()
  else:
    stack1.append(A[i])
    i += 1
  while len(stack1)<2 and i<=N-1:
    stack1.append(A[i])
    i += 1

# 下側凸包
stack2 = [A[0],A[1]]
i = 2
while len(stack2)>=2 and i<=N-1:
  if cross(stack2[-2], stack2[-1], A[i]) <= 0:
    stack2.pop()
  else:
    stack2.append(A[i])
    i += 1
  while len(stack2)<2 and i<=N-1:
    stack2.append(A[i])
    i += 1
