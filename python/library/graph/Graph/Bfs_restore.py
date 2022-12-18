"""
復元ありBFS
https://atcoder.jp/contests/tessoku-book/tasks/tessoku_book_ei
"""
import sys; input = sys.stdin.readline
I = lambda:map(int,input().split())
from collections import*
INF = 10**18
class BFS:
    def __init__(self, N, M=-1):
        self.V = N
        if M>=0: self.E = M
        self.edge = [[] for _ in range(self.V)]
        # self.edge_dic = {}

    def add_edges(self, ind=1, bi=False):
        for i,(a,*A) in enumerate(tuple(I()) for _ in range(self.E)):
            a -= ind; b = A[0] - ind
            atob,btoa = (b,a) if len(A) == 1 else ((A[1],b),(A[1],a))
            self.edge[a].append(atob)
            # self.edge_dic[(a,b)] = i
            if bi:
                self.edge[b].append(btoa)
                # self.edge_dic[(b,a)] = i

    def add_edge(self, a, b, cost=None, ind=1, bi=False):
        a -= ind; b -= ind
        atob,btoa = (b,a) if cost is None else ((cost,b),(cost,a))
        self.edge[a].append(atob)
        if bi: self.edge[b].append(btoa)

    def bfs(self, s, g=-1, zero_one=False):
        """
        zero_one=Falseなら通常のBFS、Trueなら01-BFS
        """
        #step1(初期化)
        que = deque([s])
        self.dists = [INF]*self.V
        # self.dists = defaultdict(lambda: INF)
        self.dists[s]=0
        self.prev = [-1]*self.V
        #step2(ループ)
        while len(que):
            #step2-1(queから頂点を出す)
            v = que.popleft()
            #step2-2(vがgと一致していたらgの最短距離が確定)
            if v==g: return self.dists[v]
            #step2-3(隣接頂点をループ)
            for u in self.edge[v]:
                #step2-3-1(ndistを計算)
                weight = 1
                ndist = self.dists[v] + weight
                #step2-3-2(ndist>=dists配列値なら意味がないのでスキップ)
                if ndist >= self.dists[u]: continue
                #step2-3-3(dists配列にndistをset)
                self.dists[u] = ndist
                #step2-3-4(queに隣接頂点を入れる)
                if zero_one:
                    if weight:
                        que.append(u)
                    else:
                        que.appendleft(u)
                else:
                    que.append(u)
                self.prev[u]=v
        return -1

N,M = I()
G = BFS(N,M)
G.add_edges(ind=1,bi=True)
G.bfs(s=0, g=N-1, zero_one=False)

# 頂点の場合
ans = [N]
now = N-1
while now!=0:
    now = G.prev[now]
    ans.append(now+1)
print(*ans[::-1])

# 辺の場合
# ans = []
# now = N-1
# while now!=0:
#     pre = G.prev[now]
#     ans.append(G.edge_dic[(pre,now)])
#     now = pre
# print(*ans[::-1])