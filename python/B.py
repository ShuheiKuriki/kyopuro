N, K = map(int, input().split())
lis = [0]*(2*N+1)
for i in range(1,2*N+1):
  lis[i] = N-abs(N+1-i)
ans = 0
for i in range(2*N+1):
  if 0<=i+K<=2*N:
    ans += lis[i]*lis[i+K]
print(ans)
