A, B, C = map(int, input().split())
mod = 998244353
ans = A*(A+1)*B*(B+1)*C*(C+1)//8%mod
print(ans)