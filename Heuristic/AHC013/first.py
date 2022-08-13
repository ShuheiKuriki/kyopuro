import random
import sys
from copy import deepcopy

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

    def _move(self, lim=None):
        if lim is None: lim = self.K * 50
        moves = []
        for _ in range(lim):

            i, j = random.randint(0, self.N-1), random.randint(0, self.N-1)
            if self.C[i][j] == 0: continue

            v = random.randint(0, 3)
            ni, nj = i + self.di[v], j + self.dj[v]
            if not (0 <= ni < self.N and 0 <= nj < self.N): continue
            if self.C[ni][nj] != 0: continue

            # コンピュータを移動
            self.C[i][j], self.C[ni][nj] = 0, self.C[i][j]
            moves.append([i, j, ni, nj])

        return moves

    def _connect(self, lim: int):
        connects = []

        def can_connect(i, j, v):
            ni = i + self.di[v]
            nj = j + self.dj[v]
            while ni < self.N and nj < self.N:
                if self.C[ni][nj] == 0:
                    ni += self.di[v]
                    nj += self.dj[v]
                    continue
                return self.C[ni][nj] == self.C[i][j]
            return False

        def do_connect(i, j, v):
            ni, nj = i + self.di[v], j + self.dj[v]
            while ni < self.N and nj < self.N:
                if self.C[ni][nj] == 0:
                    self.C[ni][nj] = self.USED
                elif self.C[ni][nj] == self.C[i][j]:
                    connects.append([i, j, ni, nj])
                    return
                else:
                    raise AssertionError()
                ni += self.di[v]
                nj += self.dj[v]

        for i in range(self.N):
            for j in range(self.N):
                if self.C[i][j] in (0, self.USED): continue
                for v in [0, 1]:
                    if can_connect(i, j, v):
                        do_connect(i, j, v)
                        if len(connects) >= lim:
                            return connects
        return connects

    def solve(self):
        # create random moves
        moves = self._move()
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

def calc_score(N, K, C, res: Result):
    for v in res.moves:
        i, j, ni, nj = v
        assert 1 <= C[i][j] <= K
        assert C[ni][nj] == 0
        C[ni][nj] = C[i][j]
        C[i][j] = 0

    uf = UnionFind(N*N)
    for v in res.connects:
        i, j, ni, nj = v
        p1 = i*N+j
        p2 = ni*N+nj
        assert 1 <= C[i][j] <= K
        assert 1 <= C[ni][nj] <= K
        uf.union(p1, p2)

    computers = []
    for i in range(N):
        for j in range(N):
            if 1 <= C[i][j] <= K:
                computers.append(i*N+j)

    score = 0
    for i in range(len(computers)):
        for j in range(i + 1, len(computers)):
            c1 = computers[i]
            c2 = computers[j]
            if uf.find(c1) != uf.find(c2):
                continue

            if C[c1//N][c1%N] == C[c2//N][c2%N]:
                score += 1
            else:
                score -= 1

    return max(score, 0)


def print_answer(res: Result):
    print(len(res.moves))
    for arr in res.moves:
        print(*arr)
    print(len(res.connects))
    for arr in res.connects:
        print(*arr)


def main():
    N, K = map(int, input().split())
    C = [list(map(int, list(input()))) for _ in range(N)]

    solver = Solver(N, K, deepcopy(C))
    res = solver.solve()
    print(f"Score = {calc_score(N, K, deepcopy(C), res)}", file=sys.stderr)

    print_answer(res)


if __name__ == "__main__":
    main()
