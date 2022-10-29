# DP時の演算に逆元がないモノイドに対する全方位木DP
# verify: https://atcoder.jp/contests/dp/tasks/dp_v
import sys; input = sys.stdin.readline
I = lambda:map(int,input().split())
from collections import *
class Tree:
    def __init__(self, N, merge, add_root, id):
        self.V = N
        self.edge = [[] for _ in range(N)]
        self.order = []
        self.merge = merge
        self.add_root = add_root
        self.id = id
    
    def add_edges(self, ind=1, bi=True):
        for a,*A in [tuple(I()) for _ in range(N-1)]:
            a -= ind; b = A[0] - ind
            atob,btoa = (b,a) if len(A) == 1 else ((A[1],b),(A[1],a))
            self.edge[a].append(atob)
            if bi: self.edge[b].append(btoa)

    def add_edge(self, a, b, cost=None, ind=1, bi=True):
        a -= ind; b -= ind
        atob,btoa = (b,a) if cost is None else ((cost,b),(cost,a))
        self.edge[a].append(atob)
        if bi: self.edge[b].append(btoa)

    def rerooting(self, start):
        stack = deque([start])
        self.parent = [self.V]*self.V; self.parent[start] = -1
        self.order.append(start)
        #記録したい値の配列を定義
        self.dp = [self.id]*self.V
        while stack:
            v = stack.pop()
            for u in self.edge[v]:
                if u==self.parent[v]: continue
                self.parent[u]=v
                stack.append(u); self.order.append(u)
        for v in self.order[::-1]:
            for u in self.edge[v]:
                if u==self.parent[v]: continue
                self.dp[v] = self.merge(self.dp[v], self.add_root(self.dp[u]))
        p_value = [self.id]*self.V #親側の値
        for v in self.order:
            cumL = [self.id]*(len(self.edge[v])+1)
            cumR = [self.id]*(len(self.edge[v])+1)
            for i,u in enumerate(self.edge[v]):
                if u==self.parent[v]:
                    cumL[i+1] = self.merge(cumL[i], self.add_root(p_value[v]))
                else:
                    cumL[i+1] = self.merge(cumL[i], self.add_root(self.dp[u]))
            for i,u in enumerate(self.edge[v][::-1]):
                if u==self.parent[v]:
                    cumR[-i-2] = self.merge(cumR[-i-1], self.add_root(p_value[v]))
                else:
                    cumR[-i-2] = self.merge(cumR[-i-1], self.add_root(self.dp[u]))
            for i,u in enumerate(self.edge[v]):
                if u==self.parent[v]: continue
                p_value[u] = self.merge(cumL[i], cumR[i+1])
                self.dp[u] = self.merge(self.dp[u], self.add_root(p_value[u]))

def merge(a, b): return a+b

#mergeの直前にする操作、rerootingのためにmerge前は寸止めしておく
def add_root(a): return a+1

id = 0
N = int(input())
G = Tree(N, merge, add_root, id)
G.add_edges(ind=1, bi=True)
G.rerooting(0)
print(*G.dp, sep='\n')
