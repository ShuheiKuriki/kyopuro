from random import *
from math import exp,pi,cos,sin
M=100
def dot(A,B): return sum(a*b for a,b in zip(A,B))
def sub(A,B): return [A[0]-B[0],A[1]-B[1]]
def dist(P,Q): return dot(sub(P,Q),sub(P,Q))**.5
#半径計算
def calc(lis):
    res=1
    xsorted=sorted(lis)
    for i,(x1,y1) in enumerate(xsorted):
        res = min(res, 1-dist((x1,y1),(0,0)))
        for x2,y2 in xsorted[i+1:]:
            if x2-x1>res*2:break
            res = min(res, dist((x1,y1),(x2,y2))/2)
    return res
#ランダム初期解
def get_init(cnt):
    centers=[(0,0)]*M
    res=0
    for _ in range(cnt):
        new_centers=[0]*M
        for i in range(M):
            r,theta=random(),2*pi*random()
            new_centers[i]=(r*cos(theta),r*sin(theta))
        r=calc(new_centers)
        if r>res:
            centers=new_centers
            res=r
    # centers = [tuple(map(float, input().split())) for _ in range(100)]
    return centers
centers=get_init(100)
r=calc(centers)
def get_temp(t):
    start = eps*0.07
    end = eps*0.07
    return start*(1-t)+end*t
def get_prob(new,pre,temp):
    # print(exp((new-pre)/temp))
    return exp((new-pre)/temp)
T = 10001
from time import time
start = time()
for i in range(T+1):
    eps=10**(-1*(1-i/T)-2*i/T)
    new_centers = centers[:]
    for j in sample(list(range(M)),k=M):
        dx,dy=eps*(random()-0.5),eps*(random()-0.5)
        cx,cy=centers[j]
        new_centers[j] = cx+dx,cy+dy
    nr = calc(new_centers)
    # if i%1000==0:
        # print(i,r,time()-start)
    if get_prob(nr,r,get_temp(i/T))>random():
        centers = new_centers
        # for cx,cy in centers:
            # print(cx,cy)
        r = nr
        # print(i,r)
for cx,cy in centers:
    print(cx,cy)
# print(r)