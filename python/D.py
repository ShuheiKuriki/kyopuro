mod = 998244353
N, K = map(int, input().split())
dp = [[0]*(N+1) for _ in range(N+1)]
dp[0][0] = 1
for i in range(1,N+1):
  for j in range(1,N+1):
    k = j - 1
    while k <= i:
      dp[i][j] += dp[i - 1][k]
      dp[i][j] %= mod
      k = k * 2 + 1
ans = dp[N][K]%mod
print(ans)