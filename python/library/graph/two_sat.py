# 強連結成分分解(SCC): グラフGに対するSCCを行う
class SCC:
    def __init__(self, N, M=0):
        self.V = N
        self.E = M
        self.edge = [[] for _ in range(self.V)]
        self.edge_rev = [[] for _ in range(self.V)]
        self.v_to_g = [None]*self.V
        self.label = 0
    
    def add_edges(self, ind=1):
        for i in range(self.E):
            a,b = map(int, input().split())
            a -= ind; b -= ind
            self.edge[a].append(b)
            self.edge_rev[b].append(a)
    
    def add_edge(self, a, b):
        self.edge[a].append(b)
        self.edge_rev[b].append(a)
    
    def scc(self):
        order = []
        used = [0]*self.V
        def dfs(s):
            stack = [s]; used[s] = 1
            while stack:
                v = stack[-1]
                for u in self.edge[v]:
                    if not used[u]:
                        used[u] = 1; stack.append(u); break
                else:
                    stack.pop(); order.append(v)
        def rdfs(s, col):
            stack = [s]; self.v_to_g[s] = col; used[s] = 1
            while stack:
                v = stack.pop()
                for u in self.edge_rev[v]:
                    if not used[u]:
                        self.v_to_g[u] = col; used[u] = 1; stack.append(u)
        for i in range(self.V):
            if not used[i]:
                dfs(i)
        used = [0]*self.V
        for s in order[::-1]:
            if not used[s]:
                rdfs(s, self.label); self.label += 1

import sys
input = sys.stdin.readline
N, D = map(int, input().split())
X,Y = [0]*N,[0]*N
for i in range(N):
    X[i],Y[i] = map(int, input().split())
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