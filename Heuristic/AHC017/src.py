"""
ダイクストラ法:単一始点最短経路問題、非負辺、計算量O(ElogV)
"""
import sys; input = sys.stdin.readline
I = lambda:map(int,input().split())
from heapq import*
from random import*
from time import*
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

    def dijkstra_heap(self, s, ind=0):
        s -= ind
        goal = len(nearby[s])
        # goal = N-1
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
        return res + INF * (goal-cnt)
    
    def get_pseudo_score(self):
        return sum(self.dijkstra_heap(s)for s in range(self.V))

def get_dist(u,v):
    ux,uy = XY[u]
    vx,vy = XY[v]
    return (ux-vx)**2+(uy-vy)**2

start = time()
N,M,D,K = I()
A = [0]*M
edges = [0]*M
for i in range(M):
    u,v,w = I()
    A[i] = (i,u-1,v-1,w)
    edges[i] = (u-1,v-1,w)
XY = [tuple(I()) for _ in range(N)]
nearby = [set() for _ in range(N)]
check_radius = max(8000, min(35000, 15000 * (750**1.5*2000**2*15**1.5) / (N**1.5*M**2*D**1.5)))
errprint(f"check_radius:{check_radius}")
for i in range(N):
    for j in range(i):
        if get_dist(i,j) <= check_radius:
            nearby[i].add(j)
            nearby[j].add(i)
errprint(f"nearby_min:{min(len(nearby[i])for i in range(N))},nearby_max:{max(len(nearby[i])for i in range(N))}")
errprint(f"K:{K}")
Gs = [Graph(N,M)for _ in range(D)]
for d in range(D):
    for _,u,v,w in A:
        Gs[d].add_edge(u,v,cost=w)
ans = [-1]*M
final_ans = ans[:]
C = [0]*D
rands = list(range(D))
min_score = INF*N*(N-1)
for r in range(5):
    for i,u,v,w in A:
        scores = []
        shuffle(rands)
        # T = int(t)
        # T = len(cnt_list)
        if r > 0:
            pre_day = ans[i]
            Gs[ans[i]].add_edge(u,v,cost=w)
            C[pre_day] -= 1
        for d in range(D):
            if C[d] >= K: continue
            pre_score = Gs[d].dijkstra_heap(u)
            Gs[d].delete_edge(u,v,cost=w)
            aft_score = Gs[d].dijkstra_heap(u)
            scores.append((aft_score - pre_score, rands[d], d))
            Gs[d].add_edge(u,v,cost=w)
        min_day = min(scores)[2]
        # else:
            # min_day = cnt_list[0][1]
        Gs[min_day].delete_edge(u,v,cost=w)
        final_ans[i] = ans[i] = min_day
        C[min_day] += 1
        if i%300==0:
            errprint(f"i:{i},T:{len(scores)},time:{time()-start}")
            if time()-start > 20:
                if r == 0:
                    for j in range(i+1,M):
                        for d in range(D):
                            if C[d]<K:
                                final_ans[j]=ans[j]=d
                                C[d]+=1
                                break
                exit(print(*[a+1 for a in final_ans]))
            if r > 0:
                total_score = sum(Gs[d].get_pseudo_score()for d in range(D))
                if total_score < min_score:
                    final_ans = ans[:]
                    min_score = total_score
                errprint(f"score:{total_score}")
        if r > 0 and time()-start > 20:
            exit(print(*[a+1 for a in final_ans]))
        # cnt_list = sorted((c+(d==min_day),d) for c,d in cnt_list if c+(d==min_day) < K)
print(*[a+1 for a in final_ans])