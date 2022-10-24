import sys; input = sys.stdin.readline
I = lambda:map(int,input().split())
N,M,D = I();A = sorted(I());MOD = 10**9+7
N -= 1
from collections import *
dic = defaultdict(lambda:1)
ans = (N//D * (N//D+1) // 2 * D + (N//D+1) * (N%D+1)) % MOD
for a in A:
    a -= 1
    q,r = divmod(a,D)
    p = dic[r]+q
    dic[r] -= p
    ans -= p * ((N-a)//D+1)
    ans %= MOD
print(ans)