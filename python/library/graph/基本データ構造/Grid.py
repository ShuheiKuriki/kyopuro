import sys
sys.setrecursionlimit(10**7)
from collections import deque
class Grid:
    def __init__(self, H, W, typ='str'):
        self.H = H; self.W = W
        self.dh = [0,1,0,-1]; self.dw = [1,0,-1,0]
        if typ=='str': self.grid = [input() for _ in range(H)]
        elif typ=='int': self.grid = [list(map(int, sys.stdin.buffer.readline().split())) for _ in range(H)]
        self.ans = [[0]*W for _ in range(H)]

    def bfs(self, sh, sw, gh=-1, gw=-1, ind=0):
        sh -= ind; sw -= ind; gh -= ind; gw -= ind;
        que = deque([(sh,sw)])
        self.min_cost = [[-1]*W for _ in range(H)]; self.min_cost[sh][sw]=0
        while len(que)>0:
            h,w = que.popleft()
            for i in range(4):
                h0 = h+self.dh[i]; w0 = w+self.dw[i]
                if not (0<=h0<self.H and 0<=w0<self.W): continue
                if (h0,w0) == (gh,gw): return self.min_cost[h][w]+1
                if self.grid[h0][w0]=='.' and self.min_cost[h0][w0]==-1:
                    self.min_cost[h0][w0]=self.min_cost[h][w]+1
                    que.append((h0,w0))
        return -1

    def dp(self, h, w):
        # print(h,w)
        if self.ans[h][w]>0: return self.ans[h][w]
        self.ans[h][w] = 1
        for i in range(4):
            h0 = h+self.dh[i]; w0 = w+self.dw[i]
            if not (0<=h0<self.H and 0<=w0<self.W): continue
            if self.grid[h][w]<self.grid[h0][w0]:
                self.ans[h][w] += self.dp(h0,w0)
        return self.ans[h][w]


H, W = map(int, input().split())
G = Grid(H,W)
ans = 0
for h in range(H):
    for w in range(W):
        ans += G.dp(h,w)
print(ans)