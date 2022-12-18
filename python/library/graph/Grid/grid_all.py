import sys; input = sys.stdin.readline
I = lambda:map(int,input().split())
# sys.setrecursionlimit(10**7)
from collections import*
from heapq import*
INF = 10**18
class Grid:
    def __init__(self, H, W, typ='str'):
        self.H = H; self.W = W
        self.dh = [0,1,0,-1]; self.dw = [1,0,-1,0]
        if typ=='str':
            self.grid = [input()[:-1] for _ in range(H)]
        elif typ=='int':
            self.grid = [list(I()) for _ in range(H)]
        self.ans = [[0]*W for _ in range(H)]

    #01BFSならstd=False
    def bfs(self,sh, sw, gh=-1, gw=-1, ind=0, std=True):
        #step1(初期化)
        sh-=ind; sw-=ind; gh-=ind; gw-=ind;
        que = deque([(sh,sw)])
        self.dists = [[INF]*self.W for _ in range(self.H)]
        self.dists[sh][sw]=0
        #step2(ループ)
        while len(que)>0:
            #step2-1(queから頂点を出す)
            h,w = que.popleft()
            #step2-2(vがgと一致していたらgの最短距離が確定)
            if (h,w) == (gh,gw): return self.dists[h][w]
            #step2-3(隣接頂点をループ)
            for i in range(4):
                #step2-3-0(移動後が移動できない位置ならスキップ)
                h0 = h+self.dh[i]; w0 = w+self.dw[i]
                if not (0<=h0<self.H and 0<=w0<self.W): continue
                if self.grid[h0][w0]!='.': continue
                #step2-3-1(ndistを計算)
                weight = 1
                ndist = self.dists[h][w] + weight
                #step2-3-2(ndist>=dists配列値なら意味がないのでスキップ)
                if ndist >= self.dists[h0][w0]: continue
                #step2-3-3(dists配列にndistをset)
                self.dists[h0][w0]=ndist
                #step2-3-4(queに隣接頂点を入れる)
                if std or weight: que.append((h0,w0))
                else: que.appendleft((h0,w0))
        return -1

    def dijkstra_heap(self, sh, sw, gh=-1, gw=-1, ind=0):
        #step1(初期化)
        sh-=ind; sw-=ind; gh-=ind; gw-=ind;
        que = [(0,sh,sw)]
        self.dists = [[INF]*self.W for _ in range(self.H)]
        self.dists[sh][sw]=0
        #step2(ループ)
        while len(que)>0:
            #step2-1(queから頂点を出す)
            dist,h,w = heappop(que)
            #step2-1-1(dist>dists[v]なら古い情報なのでスキップ)
            if dist > self.dists[h][w]: continue
            #step2-2(vがgと一致していたらgの最短距離が確定)
            if (h,w) == (gh,gw): return self.dists[h][w]
            #step2-3(隣接頂点をループ)
            for i in range(4):
                #step2-3-0(移動後が移動できない位置ならスキップ)
                h0 = h+self.dh[i]; w0 = w+self.dw[i]
                if not (0<=h0<self.H and 0<=w0<self.W): continue
                if self.grid[h0][w0]!='.': continue
                #step2-3-1(ndistを計算)
                weight = 1
                ndist = self.dists[h][w]+weight
                #step2-3-2(ndist>=dists配列値なら意味がないのでスキップ)
                if ndist >= self.dists[h0][w0]: continue
                #step2-3-3(dists配列にndistをset)
                self.dists[h0][w0]=ndist
                #step2-3-4(queに隣接頂点を入れる)
                heappush(que,(ndist,h0,w0))
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


H, W = I()
G = Grid(H,W)