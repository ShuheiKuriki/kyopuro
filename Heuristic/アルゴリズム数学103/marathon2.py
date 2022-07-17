import sys
input = sys.stdin.readline
from collections import deque
from random import sample,random
from math import log2
from collections import Counter
class Graph:
    def __init__(self, N, t):
        self.V = N
        self.edge = [[0]*self.V for _ in range(self.V)]
        self.order = []
        self.visited = [False]*self.V
        self.dp = [0]*self.V
        self.t = t

    def add_edge(self,cnt):
        last = 0
        for i in range(cnt):
            u,v = sample(list(range(self.V)),k=2)
            if self.edge[u][v] == 1: continue
            uu = sum(self.edge[u])
            vv = sum(self.edge[v])
            uv = self.bfs(u)[v]
            if self.get_add_prob(uu,vv,uv) > random():
                self.edge[u][v] = 1
                self.edge[v][u] = 1
                last = i
                if i+1>=1000:
                    C = self.get_dists(i+1) 
                    if max(C.keys()) <= 4: return True
            
            # if (i+1)%1000==0:
            #     C = self.get_dists(i+1) 
            #     if max(C.keys()) <= 4: return True
            #     if C[5]<=8: flag = True

            u,v = sample(list(range(self.V)),k=2)
            if self.edge[u][v]==0: continue
            uu = sum(self.edge[u])
            vv = sum(self.edge[v])
            self.edge[u][v] = 0
            self.edge[v][u] = 0
            uv = self.bfs(u)[v]
            if self.get_remove_prob(uu,vv,uv,i-last) < random():
                self.edge[u][v] = 1
                self.edge[v][u] = 1
        return False
    
    def get_add_prob(self,uu,vv,uv):
        a = (4-uu)/4
        b = (4-vv)/4
        if a<0 or b<0:
            print("NG")
            exit()
        c = log2((uv-1))*0.4
        return a*b*c

    def get_remove_prob(self,uu,vv,uv,from_last):
        a = uu/4
        b = vv/4
        c = (4-uv)/4
        if from_last>=20000:
            if uv<=4:
                return a*b
        return a*b*c
    
    def get_dists(self,i=-1,out=True):
        if i==-1:
            i = f"{self.t}th try" 
        lis = []
        for v in range(self.V):
            lis += self.bfs(v)[v+1:]
        C = Counter(lis)
        if out:
            print(self.t,i,C)
        return C

    def out(self):
        cnt = 0
        res = []
        for v in range(self.V):
            for u in range(v+1,self.V):
                if self.edge[v][u]==1:               
                    res.append(f"{v+1} {u+1}")
                    cnt += 1
        print(self.V, cnt)
        print(*res,sep="\n")
        print(*[sum(self.edge[i])for i in range(self.V)])
        
    def bfs(self, start):
        que = deque([start])
        self.min_cost = [self.V]*self.V; self.min_cost[start]=0
        while len(que)>0:
            v = que.popleft()
            for u,e in enumerate(self.edge[v]):
                if e==1 and self.min_cost[u] == self.V:
                    self.min_cost[u] = self.min_cost[v]+1
                    que.append(u)
        return self.min_cost

N, M, T = map(int, input().split())
for t in range(T):
    G = Graph(N,t+1)
    if G.add_edge(M):
        G.out()
        G.get_dists()
        exit()
print("fail")