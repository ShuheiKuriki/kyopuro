import sys; input = sys.stdin.readline
I = lambda:map(int,input().split())
N,M = I()
S = list(map(int,list(input()[:-1])))
T = list(map(int,list(input()[:-1])))

MOD = 2

fac = [1]*(MOD+1)
finv = [0]*(MOD+1)

for i in range(1, MOD+1):
    fac[i] = fac[i-1]*i % MOD
finv[MOD-1] = pow(fac[MOD-1], MOD-2, MOD)
for i in range(MOD-1, 0, -1):
    finv[i-1] = finv[i] * i % MOD

def comb_naive(n, k):
    if k < 0 or n < 0 or n - k < 0:
        return 0
    return fac[n] * finv[k] * finv[n - k] % MOD

def comb_lucas(n, k):
    ret = 1
    while n > 0:
        nq, nr = divmod(n, MOD)
        kq, kr = divmod(k, MOD)
        ret *= comb_naive(nr, kr)
        ret %= MOD
        n = nq
        k = kq
    return ret

def solve(x,y):
    if x==1:return T[y-1]
    if y==1:return S[x-1]
    res = 0
    for h in range(2,x+1):
        res ^= comb_lucas(x-h+y-2,x-h)*S[h-1]
    for w in range(2,y+1):
        res ^= comb_lucas(x-2+y-w,y-w)*T[w-1]
    return res
# for h in range(N):
#     print(*[solve(h+1,w+1)for w in range(M)])
        
print(*[solve(*I())for _ in range(int(*I()))],sep='\n')

