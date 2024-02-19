N = int(input())
S = input()
INF = 10**18
MOD = 998244353
L = N

fact = [1]*(L+1)
for i in range(L): fact[i+1] = fact[i] * (i+1) % MOD
rfact = [1]*L + [pow(fact[L], MOD-2, MOD)]
for i in range(L,0,-1): rfact[i-1] = rfact[i] * i % MOD

perm = lambda n, k: fact[n] * rfact[n-k] % MOD
comb = lambda n, k: fact[n] * rfact[n-k] % MOD * rfact[k] % MOD if n>=k else 0

dp = [[0]*(N+1)for _ in range(N+1)]
for i in range(N+1):
    dp[i][i] = 1
for l in range(2,N+1,2):
    for i in range(N+1-l):
        for left in range(i,i+l-1,2):
            for right in range(left+1,i+l,2):
                if S[left]!=S[right]:
                    a = (left-i)//2
                    b = (right-left-1)//2
                    c = (i+l-right-1)//2
                    aa = dp[i][left]
                    bb = dp[left+1][right]
                    cc = dp[right+1][i+l]
                    dp[i][i+l] += aa*bb*cc*fact[a+b+c]*rfact[a]*rfact[b]*rfact[c]%MOD
        dp[i][i+l] %= MOD
print(dp[0][N])