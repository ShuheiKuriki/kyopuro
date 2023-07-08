"""
ダイクストラ法:単一始点最短経路問題、非負辺、計算量O(ElogV)
"""
import sys; input = sys.stdin.readline
I = lambda:map(int,input().split())
from heapq import*
INF = 10**9
errprint = lambda x:print(x,file=sys.stderr)
class Graph:
    def __init__(self, N, M=-1):
        self.V = N
        if M>=0: self.E = M
        self.edge = [set()for _ in range(self.V)]

    def add_edge(self, a, b, cost=None, ind=0, bi=True):
        a -= ind; b -= ind
        atob,btoa = (b,a) if cost is None else ((cost,b),(cost,a))
        self.edge[a].add(atob)
        if bi: self.edge[b].add(btoa)

    def delete_edge(self, a, b, cost=None, ind=0, bi=True):
        a -= ind; b -= ind
        atob,btoa = (b,a) if cost is None else ((cost,b),(cost,a))
        self.edge[a].discard(atob)
        if bi: self.edge[b].discard(btoa)

    def dijkstra_heap(self, s, g=-1, ind=0):
        s -= ind; g -= ind
        goal = len(nearby[s])
        res = cnt = 0
        #step1(初期化)
        que = [(0,s)] #que:[sからの暫定最短距離,頂点]のリスト
        dists = [INF]*self.V
        dists[s] = 0
        #step2(ループ)
        while len(que):
            #step2-1(queから最短距離と頂点を出す)
            dist, v = heappop(que)
            #step2-1-1(dist>dists[v]なら古い情報なのでスキップ)
            if dist > dists[v]: continue
            #step2-2
            if v in nearby[s]:
                cnt += 1
                res += dist
                if cnt == goal:
                    return res
            #step2-3(隣接頂点をループ)
            for weight, u in self.edge[v]:
                #step2-3-1(ndistを計算)
                ndist = dists[v] + weight
                #step2-3-2(ndist>=dists配列値なら意味がないのでスキップ)
                if ndist >= dists[u]: continue
                #step2-3-3(dists配列にndistをset)
                dists[u] = ndist
                #step2-3-4(queに(ndist,隣接頂点)を入れる)
                heappush(que,(ndist,u))
        return res + INF* (goal - cnt)

def get_dist(u,v):
    ux,uy = XY[u]
    vx,vy = XY[v]
    return (ux-vx)**2+(uy-vy)**2
import sys;RL=sys.stdin.readline
from random import*
from time import*
start = time()
I=lambda:map(int,RL().split())
N,M,D,K = I()
A = [0]*M
edges = [0]*M
for i in range(M):
    u,v,w = I()
    A[i] = (i,u-1,v-1,w)
    edges[i] = (u-1,v-1,w)
XY = [tuple(I()) for _ in range(N)]
nearby = [set() for _ in range(N)]
for i in range(N):
    for j in range(i):
        if get_dist(i,j) <= 1000000:
            nearby[i].add(j)
            nearby[j].add(i)
Gs = [Graph(N,M)for _ in range(D)]
ans = [-1]*M
C = [0]*D
day_sets = [set(range(D))for _ in range(N)]
all_set = set(range(D))
for i,u,v,w in A:
    Set = day_sets[u] & day_sets[v]
    if len(Set)==0:
        ans[i] = choice(list(all_set))
    else:
        ans[i] = choice(list(Set))
    day_sets[u].discard(ans[i])
    day_sets[v].discard(ans[i])
    C[ans[i]] += 1
    if C[ans[i]] >= K:
        for v in range(N):
            day_sets[v].discard(ans[i])
        all_set.discard(ans[i])
for d in range(D):
    for i,u,v,w in A:
        if ans[i] != d:
            Gs[d].add_edge(u,v,cost=w)
t = 10000001/(M*M) + (M*M>4000000)*2
for i,u,v,w in A:
    # T = int(1+t*i/M)
    T = int(t)
    if i%300==0:
        errprint(f"i:{i},T:{T}")
    # if T > 1:
    scores = []
    C[ans[i]] -= 1
    Gs[ans[i]].add_edge(u,v,cost=w)
    cnt_list = sorted((C[d],d)for d in range(D) if C[d]<K)
    for _,d in [(0,ans[i])]+cnt_list[:(T-1)]:
    # for d in range(D):
        # if C[d] >= K: continue
        pre_score = Gs[d].dijkstra_heap(u)
        Gs[d].delete_edge(u,v,cost=w)
        aft_score = Gs[d].dijkstra_heap(u)
        scores.append((aft_score - pre_score, d))
        Gs[d].add_edge(u,v,cost=w,ind=1)
    min_day = min(scores)[1]
    Gs[min_day].delete_edge(u,v,cost=w)
    ans[i] = min_day
    C[min_day] += 1
# calc_score = lambda d1,d2,e: Gs[d1].dijkstra_heap(*edges[e][:2]) + Gs[d2].dijkstra_heap(*edges[e][:2])
# calc_scores = lambda d1,d2,es: sum(calc_score(d1,d2,e)for e in es)
# def move(e,d1,d2,calc_diff=False): #eをd1→d2と移動
#     u,v,w = edges[e]
#     if calc_diff:
#         bef = calc_score(d1,d2,e)
#     Gs[d1].add_edge(u,v,cost=w)
#     Gs[d2].delete_edge(u,v,cost=w)
#     if calc_diff:
#         aft = calc_score(d1,d2,e)
#         return aft-bef
# C = Counter(ans)
# trial = 0
# swap_cnt = move_cnt = 0
# for _ in range(trial):
#     #move:eをd1→d2へ
#     e = randint(0,M-1)
#     d1 = ans[e]
#     d2 = randint(0,D-1)
#     if d1 == d2 or C[d2] >= K: continue
#     if move(e,d1,d2,True) < 0:
#         ans[e] = d2
#         C[d2]+=1; C[d1]-=1
#         move_cnt += 1
#     else:
#         move(e,d2,d1)
print(*[a+1 for a in ans])
# errprint(f"swap:{swap_cnt},move:{move_cnt}")