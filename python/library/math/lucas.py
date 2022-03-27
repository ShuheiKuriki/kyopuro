MOD = 3

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