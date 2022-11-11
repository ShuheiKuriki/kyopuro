M, eps = input().split()
M, eps = int(M),float(eps)
N = 15
print(N)
L = N*(N-1)//2
p,r = divmod(L,M)
now = 0
lis = []
for k in range(M):
    lis.append(now)
    print("1" * now + "0" * (L-now))
    now += p
    if k < r: now += 1
from bisect import *
for q in range(100):
    H = input()
    c = H.count('1')
    if c >= lis[-1]:
        t = M-1
    else:
        ind = bisect_right(lis,c)
        if abs(c-lis[ind])<abs(c-lis[ind-1]):
            t = ind
        else:
            t = ind-1
    print(t)
