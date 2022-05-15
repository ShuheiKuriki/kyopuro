import sys
input = sys.stdin.readline
T = int(input())
ans = [0]*T
from collections import defaultdict, deque
M = 1<<18
cnts = defaultdict(lambda: -1)
que = deque([0])
cnts[0] = [0,0,0]
while len(que):
    v = que.popleft()
    if v*4>=M:continue
    for i in range(1,4):
        u = v*4+i
        cnts[u] = cnts[v][:]
        cnts[u][i-1] += 1
        que.append(u)
INF = float("inf")
for t in range(1,T+1):
    E, W = map(int, input().split())
    if E>10 or W>3: continue
    X = [list(map(int, input().split())) for _ in range(E)]+[[0]*W]
    dists = [[INF]*M for _ in range(E+2)]
    dists[0][0] = 0
    que = deque([(0,0)])
    while len(que):
        exer, v = que.popleft()
        if exer==E+1:
            ans[t-1] = f"Case #{t}: {dists[exer][v]}"
            break
        lis = [v//4]+[v*4+i for i in range(1,W+1)]
        lis = []
        if v>0: lis.append(v//4)
        if v*4<=M:
            for i in range(1,W+1): lis.append(v*4+i)
        for u in lis:
            if u>=M: continue
            ndist = dists[exer][v]+1
            nexer = exer
            while nexer <= E and cnts[u][:W] == X[nexer]:
                nexer += 1
            if ndist>=dists[nexer][u]:continue
            dists[nexer][u] = ndist
            que.append((nexer,u))
print(*ans, sep='\n')
