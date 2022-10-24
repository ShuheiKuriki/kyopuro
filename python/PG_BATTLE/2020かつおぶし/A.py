import sys; input = sys.stdin.readline
I = lambda:map(int,input().split())
from collections import *
class Tree:
    def __init__(self, N):
        self.V = N
        self.edge = [[] for _ in range(N)]

    def add_edges(self, ind=1, bi=True):
        for a,*A in [list(I()) for _ in range(self.V-1)]:
            a -= ind; b = A[0] - ind
            atob,btoa = (b,a) if len(A) == 1 else ((A[1],b),(A[1],a))
            self.edge[a].append(atob)
            if bi: self.edge[b].append(btoa)

    def bfs(self, s):
        #step1(初期化)
        que = deque([(s,-1)])
        res = 0
        #step2(ループ)
        while len(que):
            v, p = que.popleft()
            if v!=s and len(self.edge[v])==1: res+=1;continue
            for u in self.edge[v]:
                if u==p:continue
                que.append((u,v))
        return res

G = Tree(int(input()))
G.add_edges(ind=1, bi=True)
print(G.bfs(0))