import random
import sys
from copy import deepcopy
from tabnanny import check

random.seed(1)

class Result:

    def __init__(self, moves, connects):
        self.moves = moves
        self.connects = connects


class Solver:
    USED = -1
    di = [1, 0, -1, 0]
    dj = [0, 1, 0, -1]

    def __init__(self, N, K, C):
        self.N = N
        self.K = K
        self.C = C
        self.LIM = K * 100

    def _move(self, lim):
        moves = []
        while len(moves) < lim:
            i, j = random.randint(0, self.N-1), random.randint(0, self.N-1)
            if self.C[i][j] == 0: continue

            v = random.randint(0, 3)
            ni, nj = i + self.di[v], j + self.dj[v]
            while 0 <= ni < self.N and 0 <= nj < self.N and self.C[ni][nj] == 0 and self._count(ni,nj,v) > self._count(i,j,v):
                ni += self.di[v]; nj += self.dj[v]
            if not (0 <= ni < self.N and 0 <= nj < self.N): continue
            if self.C[ni][nj] != 0: continue

            # コンピュータを移動
            self.C[i][j], self.C[ni][nj] = 0, self.C[i][j]
            moves.append([i, j, ni, nj])

        return moves

    def _count(self, i, j, vv):
        cnt = 0
        for v in range(4):
            if (v+2)%4==vv: continue
            ni, nj = i+self.di[v], j+self.dj[v]
            while 0 <= ni < self.N and 0 <= nj < self.N:
                if self.C[ni][nj] == 0: ni += self.di[v]; nj += self.dj[v]; continue
                cnt += self.C[ni][nj] == self.C[i][j]
                break
        return cnt

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


def main():
    N, K = map(int, input().split())
    C = [list(map(int, list(input()))) for _ in range(N)]

    check_solver = Solver(N, K, deepcopy(C))
    connects = check_solver._connect(check_solver.LIM)
    con = len(connects)

    solver = Solver(N, K, deepcopy(C))
    res = solver.solve(K*100-con)
    print(f"Score = {calc_score(N, K, deepcopy(C), res)}", file=sys.stderr)

    print_answer(res)


if __name__ == "__main__":
    main()
