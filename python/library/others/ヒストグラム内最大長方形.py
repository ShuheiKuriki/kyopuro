import sys; input = sys.stdin.readline
I = lambda:map(int,input().split())
N = int(*I())
A = list(I())
L = [0]*N; R = [N-1]*N
stack = []
for i in range(N):
    while len(stack) and A[i] <= A[stack[-1]]: stack.pop()
    if len(stack): L[i] = stack[-1]+1
    stack.append(i)
stack = []
for i in range(N-1,-1,-1):
    while len(stack) and A[i] <= A[stack[-1]]: stack.pop()
    if len(stack): R[i] = stack[-1]-1
    stack.append(i)
ans = 0
for i in range(N): ans = max(ans, A[i]*(R[i]-L[i]+1))
print(ans)
