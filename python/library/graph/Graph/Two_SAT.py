# 2-SAT
# upsolve：https://atcoder.jp/contests/practice2/tasks/practice2_h
from collections import*
class SCC:
    def __init__(self, N, M=0):
        self.V = N
        self.E = M
        # self.edge = [[] for _ in range(self.V)]
        self.edge_que = [deque([]) for _ in range(self.V)]
        self.edge_rev = [[] for _ in range(self.V)]
        self.v_to_g = [None]*self.V
    
    def add_edges(self, ind=1):
        for _ in range(self.E):
            a,b = I()
            a -= ind; b -= ind
            self.edge_que[a].append(b)
            self.edge_rev[b].append(a)
        # self.edge = [list(es) for es in self.edge_que]

    def add_edge(self, a, b):
        # self.edge[a].append(b)
        self.edge_que[a].append(b)
        self.edge_rev[b].append(a)
    
    def scc(self):
        order = []
        used = [False]*self.V
        def dfs(s):
            used[s] = True; stack = [s]
            while stack:
                v = stack[-1]
                while len(self.edge_que[v]):
                    u = self.edge_que[v].popleft()
                    if used[u]: continue
                    used[u] = True; stack.append(u)
                    break
                else:
                    stack.pop(); order.append(v)
        def rdfs(s, gnum):
            used[s] = True; stack = [s]
            self.v_to_g[s] = gnum
            while stack:
                v = stack.pop()
                for u in self.edge_rev[v]:
                    if used[u]: continue
                    self.v_to_g[u] = gnum
                    used[u] = True; stack.append(u)
        for s in range(self.V):
            if used[s]: continue
            dfs(s)
        used = [0]*self.V
        self.gnum = 0
        for s in order[::-1]:
            if used[s]: continue
            rdfs(s, self.gnum)
            self.gnum += 1

import sys; input = sys.stdin.readline
I = lambda:map(int,input().split())
N, D = I()
X,Y = [0]*N,[0]*N
for i in range(N):
    X[i],Y[i] = I()
G = SCC(2*N)
for i in range(N):
    for j in range(N):
        if i==j: continue
        if abs(X[i]-X[j])<D: G.add_edge(i,j+N)
        if abs(Y[i]-Y[j])<D: G.add_edge(i+N,j)
        if abs(X[i]-Y[j])<D: G.add_edge(i,j)
        if abs(Y[i]-X[j])<D: G.add_edge(i+N,j+N)
G.scc()
ans = []
possible = 'Yes'
for i in range(0,N):
    if G.v_to_g[i]>G.v_to_g[i+N]:
        ans.append(X[i])
    elif G.v_to_g[i]<G.v_to_g[i+N]:
        ans.append(Y[i])
    else:
        possible = 'No'
        break
print(possible)
if possible=="Yes":
    print(*ans, sep='\n')