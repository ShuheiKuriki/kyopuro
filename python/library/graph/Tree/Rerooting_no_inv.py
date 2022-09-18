# DP時の演算に逆元がないモノイドに対する全方位木DP
import sys; input = sys.stdin.readline
f = lambda:map(int,input().split())
from collections import deque
class Tree:
    def __init__(self, N, merge, add_root, id):
        self.V = N
        self.edge = [[] for _ in range(N)]
        self.order = []
        self.merge = merge
        self.add_root = add_root
        self.id = id
    
    def add_edges(self, ind=1, bi=True):
        for _ in range(self.V-1):
            a,b = f()
            a -= ind; b -= ind
            self.edge[a].append(b)
            if bi: self.edge[b].append(a)

    def add_edge(self, a, b, bi=True):
        self.edge[a].append(b)
        if bi: self.edge[b].append(a)

    def dp(self, start):
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

    def rerooting(self, start):
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
  
def add_root(a): return a+1 #mergeの直前にする操作、rerootingのことを考えて平常時は寸止めしておく

id = (1,0)
N = int(input())
G = Tree(N, merge, add_root, id)
G.add_edges(ind=1, bi=True)
G.dp(0)
G.rerooting(0)
print(*G.dp, sep='\n')
