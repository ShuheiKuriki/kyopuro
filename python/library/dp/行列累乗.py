def power(x,n,mod):
    digit = len(str(bin(n)))-2
    a = len(x)
    dp = [x]*digit
    for i in range(1,digit):
        dp[i] = dot(dp[i-1],dp[i-1],mod)
    ans = [[0]*a for _ in range(a)]
    for i in range(a):
        ans[i][i] = 1
    for i in range(digit):
        if 1<<i & n:
            ans = dot(dp[i],ans,mod)
    return ans

def dot(A,B,mod):
    p = len(A)
    q = len(A[0])
    r = len(B)
    s = len(B[0])
    if q!=r:
        raise Exception('掛け算できません')
    ans = [[0]*s for _ in range(p)]
    for i in range(p):
        for j in range(s):
            for k in range(q):
                ans[i][j] += A[i][k]*B[k][j]
                ans[i][j] %= mod
    return ans

def mv(A,x,mod):
    p = len(A)
    q = len(A[0])
    r = len(x)
    if q!=r:
        raise Exception('掛け算できません')
    ans = [0]*p
    for i in range(p):
        for k in range(q):
            ans[i] += A[i][k]*x[k]
            ans[i] %= mod
    return ans

import sys;RL=sys.stdin.readline;I=lambda:map(int,RL().split())
def solve():
    N, M = I()
    init = [1,0]
    # 作用前の状態が横、作用後の状態が縦になる。逆にしないように注意！
    mat = [[1,1],[1,0]]
    ans = mv(power(mat,N-2,M),init,M)
    return ans[0]
print(solve())