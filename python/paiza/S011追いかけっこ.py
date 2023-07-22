import sys; input = sys.stdin.readline
sys.setrecursionlimit(10**6)
I = lambda:map(int,input().split())
DH = [[-1,0,1,0,1,1,-1,-1],[1,1,-1,-1]]
DW = [[0,-1,0,1,1,-1,1,-1],[1,-1,1,-1]]
INF = 10**18
N = int(*I())
kx,ky = I()
cx,cy = I()
def check(x,y):
    return 0<=x<N and 0<=y<N
# 0:先攻が次に動く,1:後攻が次に動く
dp0 = [[[[INF]*N for _ in range(N)] for _ in range(N)] for _ in range(N)]
dp1 = [[[[0]*N for _ in range(N)] for _ in range(N)] for _ in range(N)]
# cnts = [[[[(i in[0,N-1])*2+(j in[0,N-1])*2-((i in[0,N-1])*(j in[0,N-1]))for j in range(N)] for i in range(N)] for _ in range(N)] for _ in range(N)]
cnts = [[[[0]*N for _ in range(N)] for _ in range(N)] for _ in range(N)]
from collections import deque
que = deque([])
for i in range(N):
    # dp1[1][i][0][i] = 1
    # dp1[N-2][i][N-1][i] = 1
    # dp1[i][1][i][0] = 1
    # dp1[i][N-2][i][N-1] = 1
    for j in range(N):
        dp1[i][j][i][j] = 0
        que.append((i,j,i,j,1))
        for dh,dw in zip(DH[1],DW[1]):
            bx,by = i+dh,j+dw
            if check(bx,by):
                # if (i,j,bx,by)==(0,0,1,1):
                    # print(i,j,bx,by)
                cnts[i][j][bx][by] += 1
        # for dh,dw in zip(DH[0],DW[0]):
        #     bx,by = i+dh,j+dw
        #     if check(bx,by):
        #         dp0[i][j][bx][by] = 1
        #         for dh,dw in zip(DH[1],DW[1]):
        #             bx2,by2 = bx+dh,by+dw
        #             if check(bx2,by2):
        #                 if (i,j,bx2,by2)==(0,0,1,1):
        #                     print(i,j,bx2,by2)
        #                 cnts[i][j][bx2][by2] += 1
# que = deque([(1,i,0,i,1)for i in range(N)]+[(N-2,i,N-1,i,1)for i in range(N)]+[(i,1,i,0,1)for i in range(N)]+[(i,N-2,i,N-1,1)for i in range(N)])
while len(que):
    ax,ay,bx,by,p = que.popleft()
    if p==1:
        for dh,dw in zip(DH[p^1],DW[p^1]):
            nax,nay = ax+dh,ay+dw
            if check(nax,nay):
                if dp1[ax][ay][bx][by]+1 < dp0[nax][nay][bx][by]:
                    dp0[nax][nay][bx][by] = dp1[ax][ay][bx][by]+1
                    que.append((nax,nay,bx,by,p^1))
    elif p==0:
        for dh,dw in zip(DH[p^1],DW[p^1]):
            nbx,nby = bx+dh,by+dw
            if check(nbx,nby):
                cnts[ax][ay][nbx][nby] += 1
                if cnts[ax][ay][nbx][nby] == 4:
                    Max = 0
                    for dh,dw in zip(DH[p^1],DW[p^1]):
                        nbx2,nby2 = bx+dh,by+dw
                        if check(nbx2,nby2):Max = max(Max, dp0[ax][ay][nbx2][nby2])
                    if Max == INF: continue
                    dp1[ax][ay][nbx][nby] = Max
                    que.append((ax,ay,nbx,nby,p^1))
print()