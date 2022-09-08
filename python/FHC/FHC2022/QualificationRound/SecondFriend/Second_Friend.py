from collections import *
from itertools import *
I=input;f=lambda:map(int,I().split())
T = int(I())
dh = [-1,0,1,0]
dw = [0,-1,0,1]
from collections import deque
def solve(R,C,G,t):
    que = deque([])
    rock = [[0]*(C+2) for _ in range(R+2)]
    for r in range(1,R+1):
        for c in range(1,C+1):
            cnt = sum(G[r+dh[i]][c+dw[i]]=="#"for i in range(4))
            rock[r][c] = cnt
            if cnt == 3: que.append((r,c))
    while len(que):
        r,c = que.popleft()
        for i in range(4):
            nr,nc = r+dh[i],c+dw[i]
            if G[nr][nc]=="#":continue
            rock[nr][nc] += 1
            if rock[nr][nc]==3:
                if G[nr][nc]=="^":return [f"Case #{t}: Impossible"]
                que.append((nr,nc))
    que2 = deque([])
    tree = [[0]*(C+2) for _ in range(R+2)]
    for r in range(1,R+1):
        for c in range(1,C+1):
            cnt = sum(G[r+dh[i]][c+dw[i]]=="^"for i in range(4))
            tree[r][c] = cnt
            if cnt == 1: que2.append((r,c))
    while len(que2):
        r,c = que2.popleft()
        for i in range(4):
            nr,nc = r+dh[i],c+dw[i]
            if G[nr][nc]=="#":continue
            if rock[nr][nc]==3:continue
            G[nr][nc] = "^"
            tree[nr][nc] = sum(G[nr+dh[i]][nc+dw[i]]=="^"for i in range(4))
            if tree[nr][nc]==1:
                que2.append((nr,nc))
    res = [f"Case #{t}: Possible"] + ["".join(G[i][1:-1])for i in range(1,R+1)]
    return res               
    
for t in range(1,T+1):
    R,C = f()
    G = [["#"]*(C+2)] + [["#"]+list(I())+["#"]for _ in range(R)] + [["#"]*(C+2)]
    print(*solve(R,C,G,t), sep='\n')