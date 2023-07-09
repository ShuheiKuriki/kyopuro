import sys;RL=sys.stdin.readline;I=lambda:map(int,RL().split())
class Tree:
    def __init__(self, N):
        self.V = N
        self.edge = [[] for _ in range(N)]

    def add_edges(self, ind=1, bi=True):
        for a,*A in [tuple(I()) for _ in range(self.V-1)]:
            a -= ind; b = A[0] - ind
            atob,btoa = (b,a) if len(A) == 1 else ((A[1],b),(A[1],a))
            self.edge[a].append(atob)
            if bi: self.edge[b].append(btoa)

    def add_edge(self, a, b, cost=None, ind=1, bi=True):
        a -= ind; b -= ind
        atob,btoa = (b,a) if cost is None else ((cost,b),(cost,a))
        self.edge[a].append(atob)
        if bi: self.edge[b].append(btoa)

    def build_rooted_tree(self):
        for i,p in enumerate(list(I())):
            self.add_edge(p-1,i+1,ind=0,bi=False)

N = int(*I())
G = Tree(N)
G.add_edges(ind=1, bi=True)
# G.build_rooted_tree()