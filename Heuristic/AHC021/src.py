import sys;RL=sys.stdin.readline;I=lambda:map(int,RL().split())
N=30
L=10000
balls=[0]*N
now=N*(N+1)//2
for i in range(N):
    balls[i] = list(I())
    # balls[i] = list(range(now,now-i-1,-1))
    # now -= i+1
def sqrt(X):
    res = int(X**.5)
    while res**2>X:res-=1
    while (res+1)**2<=X:res+=1
    return res
def get_best_pos(n):
    res = sqrt(n)
    while res*(res+1)//2 < n:
        res += 1
    while (res-1)*res//2 > n:
        res -= 1
    return res-1
def ord1(i,j):
    if balls[i][j]<min(balls[i+1][j],balls[i+1][j+1]):
        return 0
    if balls[i+1][j]<balls[i+1][j+1]:
        k = j
    else:
        k = j+1
    balls[i][j],balls[i+1][k] = balls[i+1][k],balls[i][j]
    ans.append((i,j,i+1,k))
    return 1
from random import *
from math import exp
def adopt(diff, temp):
    return diff >= 0 or (temp>0 and exp(diff/temp) > random())
def ord2(i,j):
    temp = 0.3
    diff = get_best_pos(balls[i][j])-i
    if not adopt(diff, temp):
        return 0
    if balls[i][j] < min(balls[i+1][j],balls[i+1][j+1]):
        return 0
    if balls[i+1][j]<balls[i+1][j+1]:
        k = j
    else:
        k = j+1
    diff = (i+1)-get_best_pos(balls[i+1][k])
    if not adopt(diff, temp):
        return 0
    balls[i][j],balls[i+1][k] = balls[i+1][k],balls[i][j]
    ans.append((i,j,i+1,k))
    return 1

ans = []
while True:
    cnt=0
    for i in range(N-1):
        for j in range(i+1):
            cnt+=ord2(i,j)
    if cnt==0:break
while True:
    cnt=0
    for i in range(N-1):
        for j in range(i+1):
            cnt+=ord1(i,j)
    if cnt==0:break
ans = ans[:L]
print(len(ans))
for a in ans:
    print(*a)