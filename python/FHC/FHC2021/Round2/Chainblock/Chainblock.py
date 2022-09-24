import sys; input = sys.stdin.readline
f = lambda:map(int,input().split())
from collections import *
class Tree:
    def __init__(self, N):
        self.V = N
        self.edge = [[]for _ in range(N)]
        self.order = []
    
    def add_edges(self, ind=1, bi=True):
        for a,*A in [list(f())for _ in range(self.V-1)]:
            a -= ind; b = A[0] - ind
            atob,btoa = (b,a) if len(A) == 1 else ((A[1],b),(A[1],a))
            self.edge[a].append(atob)
            if bi: self.edge[b].append(btoa)

    def add_edge(self, a, b, cost=None, ind=1, bi=True):
        a -= ind; b -= ind
        atob,btoa = (b,a) if cost is None else ((cost,b),(cost,a))
        self.edge[a].append(atob)
        if bi: self.edge[b].append(btoa)

    def dp_dfs(self, start, A):
        res = 0
        stack = deque([start])
        self.parent = [self.V]*self.V; self.parent[start] = -1
        self.order.append(start)
        C = Counter(A)
        dp = [Counter([])for _ in range(self.V)]
        while stack:
            # 行きがけ(pre-order)
            v = stack.pop()
            for u in self.edge[v]:
                if u==self.parent[v]: continue
                self.parent[u]=v
                stack.append(u); self.order.append(u)
        for v in self.order[::-1]:
            # 帰りがけ(post-order)
            lis = []
            for u in self.edge[v]:
                if u==self.parent[v]: continue
                if len(dp[u])==0:res+=1
                lis.append((len(dp[u]),u))
            if len(lis):
                lis.sort()
                dp[v] = dp[lis[-1][1]]
                for _,u in lis[:-1]:
                    dp[v] += dp[u]
                    for k in dp[u]:
                        if dp[v][k] == C[k]:del dp[v][k]
                    dp[u] = []
            dp[v][A[v]]+=1
            if dp[v][A[v]]==C[A[v]]:del dp[v][A[v]]
        return res

def solve():
    N = int(*f())
    G = Tree(N)
    G.add_edges(ind=1, bi=True)
    return G.dp_dfs(0,list(f()))

if __name__ == '__main__':
    print(*[f"Case #{t+1}: {solve()}"for t in range(int(*f()))],sep='\n')