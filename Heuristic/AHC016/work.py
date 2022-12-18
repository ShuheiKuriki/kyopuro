from random import *
def generateArray(total,min_dist,need_size,min_group_size):
    arrs = []
    for group_size in range(1,total//min_group_size+1):
        res = bfs(total,group_size,min_dist,min_group_size)
        if len(arrs)+len(res)<need_size:
            arrs.extend(res)
        else:
            shuffle(res)
            for r in res:
                arrs.append(r)
            return arrs
    return arrs

from collections import *
from heapq import *
def bfs(total,num,min_dist,min_group_size):
    dists = defaultdict(lambda:min_dist+1)
    arr1 = [total//num]*(num-1) + [total//num+total%num]
    que = [(0,arr1)]
    dists[tuple(arr1)] = 0
    res = [arr1]
    while len(que):
        dist,arr1 = heappop(que)
        for i in range(num):
            for j in range(num):
                if i==j:continue
                if arr1[i]<=min_group_size:continue
                arr2 = arr1[:]
                arr2[i] -= 1
                arr2[j] += 1
                tup = tuple(sorted(arr2))
                ndist = dist+1
                for arr in res:
                    ndist = min(ndist,get_diff(arr,list(tup))//2)
                if ndist==0:continue
                ndist %= min_dist
                if ndist >= dists[tup]:continue
                if ndist == 0:
                    res.append(list(tup))
                dists[tup] = ndist
                heappush(que,(dists[tup],list(tup)))
    return res

def get_diff(arr1=None, arr2=None, G1=None, G2=None):
    if G1:arr1 = G1.best_arr
    if G2:arr2 = G2.best_arr
    l1,l2 = len(arr1),len(arr2)
    if l1 < l2:
        arr1 = [0]*(l2-l1)+arr1
    else:
        arr2 = [0]*(l1-l2)+arr2
    return sum(abs(a1-a2)for a1,a2 in zip(arr1,arr2))
# block = 8
# arrs = rec([],block)
# for arr in arrs:
#     print(*arr)
# print(len(arrs))

def rec(lis,Sum,Min,N):
    if Sum==N:return[lis]
    res = []
    for i in range(Min,N-Sum+1):
        res.extend(rec(lis+[i],Sum+i,i,N))
    return res

L = 100
fact = [1]*(L+1)
for i in range(L): fact[i+1] = fact[i] * (i+1)
comb = lambda n, k: fact[n] // fact[n-k] // fact[k]
eps = 0.05
N = 10
pows1 = [pow(eps,i)for i in range(N+1)]
pows2 = [pow(1-eps,i)for i in range(N+1)]
def get_multinomial():
    multinomial_prob = [[0]*(n+1)for n in range(N+1)]
    for n in range(N+1):
        for k in range(n+1):
            multinomial_prob[n][k] = comb(n,k)*pows1[k]*pows2[n-k]
    return multinomial_prob
print(get_multinomial())
# N = 30
# Min = 5
# LIS = [(n,len(rec([],0,1,n)))for n in range(11)]
# print(LIS)
# MIN=24
# print(len(generateArray(100,3,10,MIN)))
# M = 100
# for MIN in range(1,11):
#     for n in range(4,101):
#         res = generateArray(n,2)
#         if len(res)>=M:
#             N = n
#             print(f"{MIN=},{N=}")
#             break
# for N in range(4,49):
#     for Min in range(5,11):
#         arrs = rec([],0,Min)
#         print(f"{N=},{Min=},{len(arrs)}")
# for arr in arrs:
#     print(*arr)