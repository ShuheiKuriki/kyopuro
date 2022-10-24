import sys; input = sys.stdin.readline
I = lambda:map(int,input().split())
N,R = int(*I()),list(I())
M = max(R)
MOD = 998244353
dp = [1]+[0]*(N+M+1)
imos1 = [0]*(N+M+2)
imos2 = [0]*(N+M+2)
ans = 0
for i in range(N+M+1):
    imos2[i] = (imos2[i]+imos2[i-1])%MOD
    imos1[i] = (imos1[i]+imos1[i-1]+imos2[i])%MOD
    dp[i] = (dp[i]+imos1[i])%MOD
    if i<N:
        dp[i] = (dp[i]*pow((R[i]+1)*R[i]//2,MOD-2,MOD))%MOD
        imos1[i+1] = (imos1[i+1]+R[i]*dp[i])%MOD
        imos2[i+2] = (imos2[i+2]-dp[i])%MOD
        imos2[i+2+R[i]] = (imos2[i+2+R[i]]+dp[i])%MOD
    else:
        ans = (ans+(i+1)*dp[i])%MOD
print(ans)