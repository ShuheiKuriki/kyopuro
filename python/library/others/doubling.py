import sys
input = sys.stdin.readline

class Doubling:
    def __init__(self, N, A, sup):
        rep = sup.bit_length()
        table = [[0]*N for _ in range(rep)]
        table[0] = A
        for i in range(1,rep):
            for j in range(N):
                table[i][j] = table[i-1][table[i-1][j]]
        self.table = table

    # 位置xからK回移動後の値を求める
    def move(self, x, K):
        res = x
        p = 0
        while K:
            if K%2:
                res = self.table[p][res]
            p += 1
            K >>= 1
        return res

import sys; input = sys.stdin.readline
I = lambda:map(int,input().split())
N,K = I()
A = list(I())
db = Doubling(N,A,10**18)
db.move(0,K)