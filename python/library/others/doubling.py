import sys
input = sys.stdin.readline

class Doubling:
    def __init__(self, N, sup):
        self.sup = 10**18
        rep = sup.bit_length()
        table = [[0]*N for _ in range(rep)]
        # table[0] =  初期化
        for i in range(1,rep):
            for j in range(N):
                table[i][j] = table[i-1][table[i-1][j]]
        self.table = table

    # K回移動後の値を求める
    def move(self, K):
        ans = p = 0
        while K:
            if K%2:
                ans = self.table[p][ans]
            p += 1
            K >>= 1
        return ans

N, K = map(int, input().split())
db = Doubling(N,10**18)
db.move(K)