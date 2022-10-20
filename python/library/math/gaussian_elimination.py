import sys; input = sys.stdin.readline
I = lambda:map(int,input().split())
MOD = 998244353
N, M = I()
A = [[0]*M for _ in range(N)]
for i in range(N):
    input()
    for a in I(): A[i][a-1] = 1
S = list(I())

from operator import xor
cur = 0
cols = []
# 列ごとに処理
for i in range(M):
    # pivotが1となるようにスワップ
    if A[cur][i] == 0:
        k = cur+1
        while k < N and A[k][i] == 0: k += 1
        if k == N: continue
        A[cur], A[k] = A[k], A[cur]
    # その列が1になっているところを全て0にする
    for l,Mj in enumerate(A):
        if l != cur and Mj[i]>0: Mj[i:] = map(xor, Mj[i:], A[cur][i:])
    cols.append(i)
    cur += 1
    if cur==N: break # N行処理したら終了
rank = cur
panel = [0]*M
# 貪欲に決めて答えと合うかチェック
for i,c in enumerate(cols):
    if S[c]==1: panel = list(map(xor, panel, A[i]))
print(pow(2,N-rank,MOD) if panel == S else 0)