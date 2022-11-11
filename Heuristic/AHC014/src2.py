import sys; input = sys.stdin.readline
I = lambda:map(int,input().split())
from random import *

class UnionFind():
    def __init__(self, n):
        self.n = n
        self.parents = [-1] * n

    def find(self, x):
        if self.parents[x] < 0: return x
        # 経路圧縮
        self.parents[x] = self.find(self.parents[x])
        return self.parents[x]

    def union(self, x, y):
        x = self.find(x); y = self.find(y)
        if x == y: return
        # マージテク
        if self.parents[x] > self.parents[y]: x,y = y,x
        self.parents[x] += self.parents[y]
        self.parents[y] = x

N = 10
M = N*N
di = [1,0]
dj = [0,1]
f = lambda i,j:i*N+j

class CandyBox:
    def __init__(self):
        self.candies = list(I())
        self.box = [[0]*N for _ in range(N)]
        self.cnts = [self.candies.count(i+1)for i in range(3)]
        self.empties = [(i,j)for i in range(N)for j in range(N)]
        self.dirs = 'BFLR'
        
    def get_empties(self,box):
        return [(i,j)for i in range(N)for j in range(N)if box[i][j]==0]

    def calc_score(self,box):
        uf = UnionFind(M)
        for i in range(N):
            for j in range(N):
                for k in range(2):
                    ni,nj = i+di[k],j+dj[k]
                    if not (ni<N and nj<N):continue
                    if box[i][j]==box[ni][nj]>0:uf.union(f(i,j),f(ni,nj))
        score = 0
        for ij,x in enumerate(uf.parents):
            i,j = divmod(ij,N)
            if x < 0 and box[i][j] > 0:
                score += x*x
        score *= 10**6
        score /= sum(c*c for c in self.cnts)
        return round(score)

    def move(self,dir,box):
        if dir in 'FB':
            lis = [[self.box[i][j]for i in range(N)if box[i][j]>0]for j in range(N)]
            box = [[0]*N for _ in range(N)]
            for j in range(N):
                if dir=='F':
                    for i,l in enumerate(lis[j]):
                        box[i][j] = l
                else:
                    for i,l in enumerate(lis[j][::-1]):
                        box[-i-1][j] = l
        if dir in 'LR':
            lis = [[box[i][j]for j in range(N)if box[i][j]>0]for i in range(N)]
            box = [[0]*N for _ in range(N)]
            for i in range(N):
                if dir=='L':
                    for j,l in enumerate(lis[i]):
                        box[i][j] = l
                else:
                    for j,l in enumerate(lis[i][::-1]):
                        box[i][-j-1] = l
        return box

    def get_best(self,box,t,depth=0):
        trial = min(100-depth-t, 10) if depth else 1
        max_score = 0
        max_dir = ''
        for dir in self.dirs:
            score = 0
            if depth:
                empties = self.get_empties(box)
            for tt in range(trial):
                box1 = [box[i][:]for i in range(N)]
                if depth:
                    cs = sample(empties,k=min(1,len(empties)))
                    for i,(ci,cj) in enumerate(cs):
                        box1[ci][cj] = self.candies[t+depth+i]
                box1 = self.move(dir,box)
                if depth < 1 and t+depth+1<100:
                    _,_score = self.get_best(box1,t,depth+1)
                else:
                    _score = self.calc_score(box1)
                score += _score
            if score > max_score:
                max_dir = dir
                max_score = score
        return max_dir,round(max_score/trial)

    def play(self,t):
        p = int(*I())-1
        ci,cj = self.get_empties(self.box)[p]
        self.box[ci][cj] = self.candies[t]
        if t<5:
            next_dir = self.dirs[randint(0,3)]
        else:
            next_dir,_ = self.get_best(self.box,t,depth=0)
        self.box = self.move(next_dir,self.box)
        print(next_dir,flush=True)

candy_box = CandyBox()
for t in range(100):
    candy_box.play(t)
score = candy_box.calc_score(candy_box.box)
print(f'{score=}',file=sys.stderr)