"""
    Mo's Algorithm O((N+Q)√N)
    verify: https://atcoder.jp/contests/abc242/tasks/abc242_g
"""
import sys; input = sys.stdin.readline
I = lambda:map(int,input().split())
N,A,Q = int(*I()),list(I()),int(*I())
M = int(N**.5)+1
from collections import*
Mo = [defaultdict(lambda:[])for _ in range(M)]
for i in range(Q):
    l,r = I()
    Mo[(l-1)//M][r-1].append((i,l-1))
ans = [0]*Q
for i in range(M):
    C = [0]*(N+1)
    l1,r1 = 0,-1
    cnt = 0
    for r2 in sorted(Mo[i].keys()):
        for ind,l2 in Mo[i][r2]:
            if r1<=r2:
                for r in range(r1+1,r2+1):
                    # rを進める処理
                    if C[A[r]]:cnt += 1
                    C[A[r]] ^= 1
            else:
                for r in range(r1,r2,-1):
                    # rを戻す処理
                    C[A[r]] ^= 1
                    if C[A[r]]:cnt -= 1
            if l1<=l2:
                for l in range(l1,l2):
                    # lを進める処理
                    C[A[l]] ^= 1
                    if C[A[l]]:cnt -= 1
            else:
                for l in range(l1-1,l2-1,-1):
                    # lを戻す処理
                    if C[A[l]]:cnt += 1
                    C[A[l]] ^= 1
            ans[ind] = cnt
            l1,r1 = l2,r2
print(*ans, sep='\n')