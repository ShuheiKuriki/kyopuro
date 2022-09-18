#最小全域木問題、プリム法
import sys; input = sys.stdin.readline
f = lambda:map(int,input().split())
from heapq import *
def solve():
    N, M = f()
    edge = [[] for _ in range(N)]
    for _ in range(M):
        a,b,w = f()
        edge[a].append((w,b))
        edge[b].append((w,a))
    bridges = []
    heapify(bridges)
    used = [False]*N
    used[0] = True
    ans = 0
    for w,v in edge[0]:
        heappush(bridges,(w,v))
    while len(bridges)>0:
        w,v = heappop(bridges)
        if used[v]==False:
            ans += w
            used[v] = True
            for w,u in edge[v]:
                if used[u]==False:
                    heappush(bridges,(w,u))
    return ans
print(solve())