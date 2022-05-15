def binary_search(low, high, func, get_mini=True):
    #求めるのが最大値か最小値かでokとngが反転
    if get_mini:    ok, ng = high, low-1
    else:           ok, ng = low, high+1

    mid = (ok+ng)//2
    while abs(ok-ng)>1:
        if func(mid):   ok = mid
        else:           ng = mid
        mid = (ok+ng)//2
    return ok

#判定問題の条件を満たすときTrueを返す関数
def is_ok(target,X):
    return 4*X >= (2*target-1)**2

import sys,os,io
input = sys.stdin.readline
#input = io.BytesIO(os.read(0,os.fstat(0).st_size)).readline

def roundsqrt(X):
    # 単純に下限と上限を指定
    low, high = 0, X+10
    res = binary_search(low,high,func=lambda x:is_ok(x,X),get_mini=False)
    return res
    
def draw_circle_perimeter(r):
    for x in range(R+1):
        yy = roundsqrt(r*r-x*x)
        grid[x][yy] = 1
        grid[yy][x] = 1
    
T = int(input())
ans = [0]*T
up = 1
down = 0
for t in range(1,T+1):
    R = int(input())
    grid = [[0]*(R+1) for _ in range(R+1)]
    for r in range(R+1): draw_circle_perimeter(r)
    cnt = 0
    for x in range(R+1):
        for y in range(R+1):
            if 4*(x*x+y*y)<(2*R+1)**2 and grid[x][y] == 0: cnt += 4
    ans[t-1] = f"Case #{t}: {cnt}"
print(*ans, sep='\n')