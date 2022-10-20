import sys; input = sys.stdin.readline
I = lambda:map(int,input().split())
sys.setrecursionlimit(10**7)
class Grid:
    def __init__(self, H, W, typ='str'):
        self.H = H; self.W = W
        self.dh = [0,1,0,-1]; self.dw = [1,0,-1,0]
        if typ=='str': self.grid = [input()[:-1] for _ in range(H)]
        elif typ=='int': self.grid = [list(I()) for _ in range(H)]
        self.ans = [[0]*W for _ in range(H)]

    def dp_dfs_rec(self, h, w):
        # print(h,w)
        if self.ans[h][w]>0: return self.ans[h][w]
        self.ans[h][w] = 1
        for i in range(4):
            h0 = h+self.dh[i]; w0 = w+self.dw[i]
            if not (0<=h0<self.H and 0<=w0<self.W): continue
            if self.grid[h][w] < self.grid[h0][w0]:
                self.ans[h][w] += self.dp_dfs_rec(h0,w0)
        return self.ans[h][w]

H, W = I()
G = Grid(H,W)
G.dp_dfs_rec(0,0)