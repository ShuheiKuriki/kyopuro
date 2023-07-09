import sys;RL=sys.stdin.readline;I=lambda:map(int,RL().split())
H, W = I()
A = [list(I()) for _ in range(H)]
cum = [[0]*(W+1) for _ in range(H+1)]
for i in range(1,H+1):
    for j in range(1,W+1):
        cum[i][j]=cum[i-1][j]+cum[i][j-1]-cum[i-1][j-1]+A[i-1][j-1]
calc = lambda h1,w1,h2,w2: cum[h2+1][w2+1]+cum[h1][w1]-cum[h2+1][w1]-cum[h1][w2+1]
from itertools import*
CR = lambda x:combinations(range(1,x+1),2)
print(max(calc(i-1,k-1,j,l)for i,j in CR(H)for k,l in CR(W)))