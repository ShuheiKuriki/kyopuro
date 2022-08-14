from random import *
import sys
from copy import deepcopy

seed(1)

class Result:

    def __init__(self, moves, connects):
        self.moves = moves
        self.connects = connects


class Solver:
    USED = -1
    di = [1, 0, -1, 0]
    dj = [0, 1, 0, -1]

    def __init__(self, N, K, C, LIM):
        self.N = N
        self.K = K
        self.C = C
        self.LIM = LIM

    def _move(self, lim):
        moves = []
        t = 0
        while t < 10:
            for i in range(self.N):
                for j in range(self.N):
                    k = self.C[i][j]-1 # 移動させたい行のmod
                    if k == -1: continue
                    iK = i % self.K # 今いる場所
                    if iK > k:
                        if i+self.K > self.N-1 or iK - k < (k+self.K) - iK:
                            v, l = 2, iK - k
                        elif iK - k > (k+self.K) - iK:
                            v, l = 0, (k+self.K) - iK
                        else:
                            v, l = randint(0,1)*2, iK - k
                    elif iK < k:
                        if i-self.K < 0 or k - iK < iK - (k-self.K):
                            v, l = 0, k - iK
                        elif k - iK > iK - (k-self.K):
                            v, l = 2, iK - (k-self.K)
                        else:
                            v, l = randint(0,1)*2, k - iK
                    else:
                        continue
                    for ll in range(1,l+1):
                        ni, nj = i + self.di[v]*ll, j + self.dj[v]*ll
                        if not (0 <= ni < self.N and 0 <= nj < self.N): break
                        if self.C[ni][nj] != 0: break
                    else:
                        # コンピュータを移動
                        ni, nj = i, j
                        for _ in range(l):
                            nni, nnj = ni + self.di[v], nj + self.dj[v]
                            self.C[ni][nj], self.C[nni][nnj] = 0, self.C[ni][nj]
                            moves.append([ni, nj, nni, nnj])
                            ni, nj = nni, nnj
                    if len(moves) >= lim:
                        return moves
            t += 1
        return moves

    def _connect(self, lim: int):
        connects = []

        def can_connect(i, j, v):
            ni, nj = i + self.di[v], j + self.dj[v]
            while ni < self.N and nj < self.N:
                if self.C[ni][nj] == 0: ni += self.di[v]; nj += self.dj[v]; continue
                return self.C[ni][nj] == self.C[i][j]
            return False

        def do_connect(i, j, v):
            ni, nj = i + self.di[v], j + self.dj[v]
            while ni < self.N and nj < self.N:
                if self.C[ni][nj] == 0:
                    self.C[ni][nj] = self.USED
                elif self.C[ni][nj] == self.C[i][j]:
                    connects.append([i, j, ni, nj]); return
                else:
                    raise AssertionError()
                ni += self.di[v]; nj += self.dj[v]

        for i in range(self.N):
            for j in range(self.N):
                if self.C[i][j] in (0, self.USED): continue
                for v in range(2):
                    if can_connect(i, j, v):
                        do_connect(i, j, v)
                        if len(connects) >= lim: return connects
        return connects

    def solve(self, move_lim):
        # create random moves
        moves = self._move(move_lim)
        # from each computer, connect to right and/or bottom if it will reach the same type
        connects = self._connect(self.LIM - len(moves))

        return Result(moves, connects)

class UnionFind():
    def __init__(self, n):
        self.n = n
        self.parents = [-1] * n

    def find(self, x):
        if self.parents[x] < 0: return x
        # 経路圧縮
        self.parents[x] = self.find(self.parents[x])
        return self.parents[x]

    def union(self, x, y):
        x = self.find(x); y = self.find(y)
        if x == y: return
        # マージテク
        if self.parents[x] > self.parents[y]: x,y = y,x
        self.parents[x] += self.parents[y]
        self.parents[y] = x

    def same(self, x, y):
        return self.find(x) == self.find(y)

def calc_score(N, K, C, res: Result):
    # 計算量O(10^5)
    for v in res.moves:
        i, j, ni, nj = v
        assert 1 <= C[i][j] <= K
        assert C[ni][nj] == 0
        C[ni][nj], C[i][j] = C[i][j], 0

    uf = UnionFind(N*N)
    for v in res.connects:
        i, j, ni, nj = v
        p1, p2 = i*N+j, ni*N+nj
        assert 1 <= C[i][j] <= K
        assert 1 <= C[ni][nj] <= K
        uf.union(p1, p2)

    comps = [i*N+j for i in range(N) for j in range(N) if 1 <= C[i][j] <= K]

    score = 0
    for j in range(len(comps)):
        for i in range(j):
            c1, c2 = comps[i], comps[j]
            if uf.same(c1, c2): score += (C[c1//N][c1%N] == C[c2//N][c2%N]) * 2 - 1

    return max(score, 0)


def print_answer(res: Result):

    print(len(res.moves))
    for arr in res.moves: print(*arr)

    print(len(res.connects))
    for arr in res.connects: print(*arr)


def binary_search(low, high, N, K, C, get_mini=True):
    #求めるのが最大値か最小値かでokとngが反転
    ok, ng = (high, low-1) if get_mini else (low, high+1)
    mid = (ok+ng)//2
    while abs(ok-ng)>1:
        ok, ng = (mid, ng) if is_ok(mid, N, K, C) else (ok, mid)
        mid = (ok+ng)//2
    return ok


#判定問題の条件を満たすときTrueを返す関数
def is_ok(target, N, K, C):
    check_solver = Solver(N, K, deepcopy(C), K*200)
    res = check_solver.solve(target)
    l = len(res.moves) + len(res.connects)
    print(target, l, file=sys.stderr)
    print(f"Score = {calc_score(N, K, deepcopy(C), res)}", file=sys.stderr)
    return l < K * 103


def main():
    N, K = map(int, input().split())
    C = [list(map(int, list(input()))) for _ in range(N)]

    LIM = K*100
    # 単純に下限と上限を指定
    low, high = 0, LIM
    move_lim = binary_search(low,high,N,K,C,get_mini=False)

    solver = Solver(N, K, deepcopy(C), LIM)
    res = solver.solve(move_lim)
    print(move_lim, len(res.moves) + len(res.connects), file=sys.stderr)
    print(f"Score = {calc_score(N, K, deepcopy(C), res)}", file=sys.stderr)

    print_answer(res)


if __name__ == "__main__":
    main()
