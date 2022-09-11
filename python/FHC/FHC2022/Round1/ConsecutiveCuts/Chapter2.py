def z_algo(S):
    """
        S[i:N]とS自身の最長共通接頭辞長をO(N)で求める
    """
    N = len(S)
    A = [0]*N
    i = 1; j = 0
    A[0] = l = len(S)
    while i < l:
        while i+j < l and S[j] == S[i+j]:
            j += 1
        if not j:
            i += 1
            continue
        A[i] = j
        k = 1
        while l-i > k < j - A[k]:
            A[i+k] = A[k]
            k += 1
        i += k; j -= k
    return A

import sys
I=sys.stdin.readline;f=lambda:map(int,I().split())
from collections import Counter
def solve(N,K,A,B):
    if A == B:
        if N == 2 and K % 2 == 0: return "YES"
        if N != 2 and K != 1: return "YES"
    if K == 0: return "NO"
    CA = Counter(A)
    CB = Counter(B)
    if CA != CB: return "NO"
    ZT = z_algo(A+B+B)
    if max(ZT[N+1:N*2])>=N and (N > 2 or K % 2 == 1): return "YES"
    return "NO"

if __name__ == '__main__':
    T = int(I())
    ans = [""]*T
    for t in range(1,T+1):
        N,K = f()
        A,B = list(f()),list(f())
        ans[t-1] = f"Case #{t}: {solve(N,K,A,B)}"
    print(*ans, sep='\n')