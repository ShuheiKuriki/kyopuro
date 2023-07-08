import sys;RL=sys.stdin.readline;I=lambda:map(int,RL().split())
N=30
L=10000
balls=[0]*N
M=N*(N+1)//2
pos=[0]*M
for i in range(N):
    balls[i] = list(I())
    for j in range(i+1):
        pos[balls[i][j]] = (i,j)
def align(b):
    while True:
        i,j = pos[b]
        if i==0:break
        x=balls[i-1][j] if j<i else -1
        y=balls[i-1][j-1] if j>0 else -1
        k = j if x>y else j-1
        if b > balls[i-1][k]:break
        pos[balls[i][j]] = (i-1,k)
        pos[balls[i-1][k]] = (i,j)
        balls[i][j],balls[i-1][k] = balls[i-1][k],balls[i][j]
        ans.append((i,j,i-1,k))
    return
ans = []
for b in range(M):
    align(b)
ans = ans[:L]
print(len(ans))
for a in ans:
    print(*a)