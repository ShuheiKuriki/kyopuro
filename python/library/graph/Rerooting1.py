import sys
input = sys.stdin.readline
from collections import deque
class Tree:
    def __init__(self, N, merge, op, id):
        self.V = N
        self.edge = [[] for _ in range(N)]
        self.order = []
        self.merge = merge
        self.op = op
        self.id = id
    
    def add_edges(self, ind=1, bi=True):
        for i in range(self.V-1):
            a,b = map(int, input().split())
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
                self.dp[v] = self.merge(self.dp[v], self.op(self.dp[u]))

    def rerooting(self, start):
        p_value = [self.id]*self.V #親側の値
        for v in self.order:
            cumL = [self.id]*(len(self.edge[v])+1)
            cumR = [self.id]*(len(self.edge[v])+1)
            for i,u in enumerate(self.edge[v]):
                if u==self.parent[v]:
                    cumL[i+1] = self.merge(cumL[i], self.op(p_value[v]))
                else:
                    cumL[i+1] = self.merge(cumL[i], self.op(self.dp[u]))
            for i,u in enumerate(self.edge[v][::-1]):
                if u==self.parent[v]:
                    cumR[-i-2] = self.merge(cumR[-i-1], self.op(p_value[v]))
                else:
                    cumR[-i-2] = self.merge(cumR[-i-1], self.op(self.dp[u]))
            for i,u in enumerate(self.edge[v]):
                if u==self.parent[v]: continue
                p_value[u] = self.merge(cumL[i], cumR[i+1])
                self.dp[u] = self.merge(self.dp[u], self.op(p_value[u]))

def merge(a, b): return a+b
  
def op(a): return a+1 #mergeの直前にする操作、rerootingのことを考えて平常時は寸止めしておく

id = (1,0)
N = int(input())
G = Tree(N, merge, op, id)
G.add_edges(ind=1, bi=True)
G.dp(0)
G.rerooting(0)
print(*G.dp, sep='\n')
