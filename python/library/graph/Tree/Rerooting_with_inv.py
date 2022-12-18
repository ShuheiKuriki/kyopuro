# DP時の演算に逆元がある群に対する全方位木DP
import sys; input = sys.stdin.readline
I = lambda:map(int,input().split())
from collections import*
class Tree:
    def __init__(self, N, merge, divide, add_root, id):
        self.V = N
        self.edge = [[] for _ in range(N)]
        self.order = []
        self.merge = merge
        self.divide = divide
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
                #帰りがけ処理
                self.dp[v] = self.merge(self.dp[v], self.add_root(self.dp[u]))
        for v in self.order:
            for u in self.edge[v]:
                if u==self.parent[v]: continue
                p_value = self.divide(self.dp[v], self.add_root(self.dp[u]))
                self.dp[u] = self.merge(self.dp[u], self.add_root(p_value))

def merge(a, b): return a+b
  
def divide(a, b): return a-b

def add_root(a): return a+1

id = 0
N = int(*I())
G = Tree(N, merge, divide, add_root, id)
G.add_edges(ind=1, bi=True)
G.rerooting(0)
print(*G.dp, sep='\n')
