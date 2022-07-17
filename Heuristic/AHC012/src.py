from collections import Counter
def calc_score(lineX,lineY,fruits,dists):
    nx = len(lineX)+1
    ny = len(lineY)+1
    areas = [[0]*ny for _ in range(nx)]
    for x,y in fruits:
        # 数が少ないので二分探索すると遅くなる
        ix, iy = nx-1, ny-1
        for i,lx in enumerate(lineX):
            if x < lx: ix = i; break
            elif x == lx: ix = -1; break
        for i,ly in enumerate(lineY):
            if y < ly: iy = i; break
            elif y == ly: iy = -1; break
        if ix == -1 or iy == -1: continue
        areas[ix][iy] += 1
    C = Counter([areas[i//ny][i%ny] for i in range(nx*ny)])
    score = 0
    for i in range(1,11):
        score += min(dists[i-1],C[i])
    score /= sum(dists)
    score *= 1000000
    return round(score)

from random import *
def moveLine(lines):
    num = len(lines)
    cl = randint(0,num-1) # どの線をずらすか決める
    sign = randint(0,1)*2-1 # 正方向にずらすか負方向にずらすか決める
    a,b = randint(1,20), randint(1,5) # 元の位置と隣の線の位置の内分比を決定
    # 決めた内分比の位置にずらす、一番端の場合は100ずらす
    if (cl+sign)%num==0: lines[cl] += 100*sign
    else: lines[cl] = (lines[cl]*a+lines[cl+sign]*b)//(a+b)
    return lines[:]

from math import exp
def annealing(lineX,lineY,fruits,dists,t_limit):
    start_temp = 1000
    end_temp = 100
    num = 10000
    score = 0
    for t in range(num):
        temp = (start_temp*(num-t)+end_temp*t)//num
        nlineX, nlineY = lineX[:], lineY[:]
        if randint(0,1): nlineX = moveLine(lineX[:])
        else: nlineY = moveLine(lineY[:])
        # moveLine(lineY[:])
        new_score = calc_score(nlineX,nlineY,fruits,dists)
        if new_score-score > 0 or exp((new_score-score)/temp) > random():
            lineX, lineY = nlineX, nlineY
            score = new_score
        now = time() - start_time
        # if t % 1000 == 0:
        #    print(now, score)
        if now > t_limit: break
    return lineX, lineY, score
    
from time import time
start_time = time()
N, K = map(int, input().split())
A = list(map(int, input().split()))
S = sum(A)
# kx = min(int(S**0.5*1.1), K//2)
# ky = min(int(S**0.5*1.1), K//2)
ky = 13
kx = min(int(S*1.1//ky), K-ky-2)
if kx%2==0: kx+=1
if ky%2==0: ky+=1
XYs = []
for i in range(N):
    x,y = map(int, input().split())
    XYs.append((x,y))
M = 10000
unitX = M*2//(kx+1)
unitY = M*2//(ky+1)
ans = []
lineX = [0]*kx
lineY = [0]*ky
for i in range(1,kx+1):
    coo = unitX*(-kx//2+i)
    lineX[i-1] = coo
for i in range(1,ky+1):
    coo = unitY*(-ky//2+i)
    lineY[i-1] = coo

time_limit = 2.8
lineX, lineY, score = annealing(lineX,lineY,XYs,A,time_limit)
#print(score)
for x in lineX: ans.append((x,0,x,1))
for y in lineY: ans.append((0,y,1,y))
print(len(ans))
for a in ans: print(*a)