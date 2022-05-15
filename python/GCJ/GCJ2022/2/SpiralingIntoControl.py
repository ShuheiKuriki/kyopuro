import sys,os,io
input = sys.stdin.readline
#input = io.BytesIO(os.read(0,os.fstat(0).st_size)).readline
from collections import deque
T = int(input())
ans = []
for t in range(1,T+1):
    N, K = map(int, input().split())
    M = N//2
    L = N*N
    dw = [1,0,-1,0]; dh = [0,1,0,-1]
    grid = [[0]*N for _ in range(N)]
    nd = nw = nh = 0
    for i in range(1,L+1):
        grid[nh][nw] = i
        nnh, nnw = nh + dh[nd], nw + dw[nd]
        if min(nnw,nnh)<0 or max(nnw,nnh)>=N or grid[nnh][nnw]>0:
            nd = (nd+1)%4
            nh += dh[nd]; nw += dw[nd]
        else:
            nh, nw = nnh, nnw
    #step1(初期化)
    sh=sw=0; gh=gw=M;
    que = deque([(sh,sw,0)])
    reachable = [[[0]*(N) for _ in range(N)] for _ in range(K+1)]
    reachable[sh][sw][0]=1
    #step2(ループ)
    while len(que)>0:
        #step2-1(queから頂点を出す)
        h,w,cnt = que.popleft()
        #step2-2(vがgと一致していたらgの最短距離が確定)
        if (h,w,cnt) == (gh,gw,K): break
        if cnt == K: continue
        #step2-3(隣接頂点をループ)
        for i in range(4):
            #step2-3-0(移動後が移動できない位置ならスキップ)
            h0 = h+dh[i]; w0 = w+dw[i]
            if not (0<=h0<N and 0<=w0<N): continue
            if grid[h0][w0]<grid[h][w]: continue
            #step2-3-2(ndist>=dists配列値なら意味がないのでスキップ
            if reachable[cnt+1][h0][w0]: continue
            #step2-3-3(dists配列にndistをset)
            reachable[cnt+1][h0][w0]=1
            #step2-3-4(queに隣接頂点を入れる)
            que.append((h0,w0,cnt+1))
    if not reachable[cnt][gh][gw]:
        ans.append(f"Case #{t}: IMPOSSIBLE")
        continue
    #step3(復元)
    shortcuts = []
    nh, nw = gh, gw
    for cnt in range(K-1,-1,-1):
        for i in range(4):
            h0 = nh+dh[i]; w0 = nw+dw[i]
            if not (0<=h0<N and 0<=w0<N): continue
            if grid[h0][w0]>grid[nh][nw]: continue
            if reachable[cnt][h0][w0]==0: continue
            if cnt==0 and (h0,w0) != (sh,sw): continue
            if grid[h0][w0]<grid[nh][nw]-1: shortcuts.append((grid[h0][w0],grid[nh][nw]))
            nh, nw = h0, w0
            break
    ans.append(f"Case #{t}: {len(shortcuts)}")
    for s in shortcuts[::-1]: ans.append(" ".join(map(str,s)))
print(*ans, sep='\n')