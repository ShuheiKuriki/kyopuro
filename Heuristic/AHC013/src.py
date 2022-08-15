from random import *
import sys
from copy import deepcopy
from itertools import permutations
from collections import defaultdict
from time import time
from math import exp

seed(1)

class Result:

    def __init__(self, moves, connects):
        self.moves = moves
        self.connects = connects


class Solver:
    USED = -1
    di = [1, 0, -1, 0]
    dj = [0, 1, 0, -1]

    def __init__(self, N, K, C, LIM, TIME_LIMIT=False):
        self.N = N
        self.K = K
        self.C = C
        self.LIM = LIM
        self.moves = []
        self.rev_moves = defaultdict(lambda: [])
        self.can_remove = [[0]*N for _ in range(N)]
        self.in_cnt = [[0]*N for _ in range(N)]
        self.out_cnt = [[0]*N for _ in range(N)]
        self.move_check = defaultdict(lambda: 0)
        self.connects = []
        if TIME_LIMIT: self.TIME_LIMIT = TIME_LIMIT

    def solve(self, move_lim, hill=False):

        self._move(move_lim)

        if hill: self._hill_climb()
        
        self._connect(self.LIM - len(self.moves))

        return Result(self.moves, self.connects)

    def _move(self, lim):

        def find_best():
            min_dist = 10**10
            res = []
            for perm in permutations(range(self.K), r=self.K):
                lis = list(perm)
                dist = 0
                for i in range(self.N):
                    for j in range(self.N):
                        m = lis[self.C[i][j]-1]
                        dist += min(abs(i % self.K - m), abs(i % self.K - (m+self.K)), abs(i % self.K - (m-self.K)))
                if dist < min_dist:
                    res = lis
                    min_dist = dist
            return res

        def decide_move(i, j, goals):
            gmod = goals[self.C[i][j]-1] # 移動させたい行のmod
            lis = [i % self.K, j % self.K]
            ij = 0
            smod = lis[ij]
            # if smod == gmod:
            #     ij ^= 1
            #     smod = lis[ij]
            assert smod != gmod
            if smod > gmod:
                if i+self.K > self.N-1 or smod - gmod < (gmod+self.K) - smod:
                    # 下の方が近い場合
                    v, l = ij + 2, smod - gmod
                elif smod - gmod > (gmod+self.K) - smod:
                    # 上の方が近い場合
                    v, l = ij, (gmod+self.K) - smod
                else:
                    # 同じ場合
                    v, l = ij + randint(0,1)*2, smod - gmod
            elif smod < gmod:
                if i-self.K < 0 or gmod - smod < smod - (gmod-self.K):
                    # 上の方が近い場合
                    v, l = ij, gmod - smod
                elif gmod - smod > smod - (gmod-self.K):
                    # 下の方が近い場合
                    v, l = ij+2, smod - (gmod-self.K)
                else:
                    # 同じ場合
                    v, l = ij + randint(0,1)*2, gmod - smod
            return v,l

        goals = find_best()
        t = 0
        while t < 10:
            for c in range(1,self.K+1):
                for i in range(self.N):
                    for j in range(self.N):
                        if self.C[i][j] != c: continue
                        if goals[c-1] == i % self.K: continue
                        v, l = decide_move(i, j, goals)
                        for ll in range(1,l+1):
                            ni, nj = i + self.di[v]*ll, j + self.dj[v]*ll
                            if not (0 <= ni < self.N and 0 <= nj < self.N): break
                            if self.C[ni][nj] != 0: break
                        else:
                            # コンピュータを移動
                            ni, nj = i, j
                            for _ in range(l):
                                nni, nnj = ni + self.di[v], nj + self.dj[v]
                                self._move_computer(ni, nj, nni, nnj)
                                ni, nj = nni, nnj
                        if len(self.moves) >= lim:
                            # print("t", t, file=sys.stderr)
                            return self.moves
            t += 1
        # print("t", t, file=sys.stderr)
        return self.moves

    def _connect(self, lim: int):

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
                    self.connects.append((i, j, ni, nj)); return
                else:
                    raise AssertionError()
                ni += self.di[v]; nj += self.dj[v]

        for c in range(1,self.K+1):
            for i in range(self.N):
                for j in range(self.N):
                    # if self.C[i][j] in (0, self.USED): continue
                    if self.C[i][j] != c: continue
                    for v in range(2):
                        if can_connect(i, j, v):
                            do_connect(i, j, v)
                            if len(self.connects) >= lim: return self.connects
        return self.connects

    def _hill_climb(self):

        # moveを追加
        def add_move():
            i, j, v = randint(0,self.N-1), randint(0,self.N-1), randint(0,3)
            ni, nj = i + self.di[v], j + self.dj[v]
            diff = 0
            for _ in range(10):
                while not (0 <= ni < self.N and 0 <= nj < self.N) or self.move_check[(i,j,ni,nj)] \
                        or self.C[i][j] == 0 or self.C[ni][nj] != 0:
                    i, j, v = randint(0,self.N-1), randint(0,self.N-1), randint(0,3)
                    ni, nj = i + self.di[v], j + self.dj[v]
                bef_score = eval(i, j)
                self._move_computer(i, j, ni, nj)
                aft_score = eval(i, j)
                if aft_score >= bef_score:
                    diff = aft_score - bef_score
                    return diff, i, j, ni, nj
                else:
                    self._undo_move(ni, nj, i, j)
            raise Exception

        # moveを削除
        def del_move():
            del_choice = [(i,j) for i in range(self.N) for j in range(self.N) if self.can_remove[i][j]]
            for _ in range(10):
                i, j = choice(del_choice)
                old_i, old_j = self.rev_moves[(i,j)][-1]
                if self.out_cnt[i][j] > 0: continue
                if self.in_cnt[old_i][old_j] > 0: continue
                if not 1 <= self.C[i][j] <= self.K: continue
                if 1 <= self.C[old_i][old_j] <= self.K: continue
                break
            else:
                raise Exception
            bef_score = eval(i, j)
            # print(i,j,old_i,old_j,file=sys.stderr)
            self._undo_move(i, j, old_i, old_j, last=False)
            aft_score = eval(i, j)
            diff = aft_score - bef_score
            return diff, i, j, old_i, old_j

        def eval(i, j):
            width = 3
            il, ir = max(0,i-width), min(self.N-1,i+width)
            jl, jr = max(0,j-width), min(self.N-1,j+width)
            score = 0
            for i in range(il,ir+1):
                for j in range(jl,jr+1):
                    c = self.C[i][j]
                    for ii in range(i+1,ir+1):
                        cc = self.C[ii][j]
                        if cc > 0:
                            if c == cc: score += 1
                            break
                    for jj in range(j+1,jr+1):
                        cc = self.C[i][jj]
                        if cc > 0:
                            if c == cc: score += 1
                            break
            # print(il,ir,jl,jr,score,file=sys.stderr)
            return score

        global start
        update = 0
        s_temp, e_temp = 0.5, 0.1
        max_step = 20000
        diff = 0
        for step in range(max_step):
            if step % 1000 == 0:
                now = time()-start
                print(step, update, file=sys.stderr)
                if now >= self.TIME_LIMIT: break

            try:
                add_diff, add_i, add_j, add_ni, add_nj = add_move()
            except Exception:
                continue

            try:
                del_diff, del_i, del_j, del_oi, del_oj = del_move()
            except Exception:
                self._undo_move(add_ni, add_nj, add_i, add_j, last=False)
                continue

            temp = (s_temp*(max_step-step)+e_temp*step)/max_step
            diff = del_diff + add_diff
            if diff > 0 or exp((diff-2)/temp) > random():
            # if diff > 0:
                # 遷移を採用する
                update += 1
            else:
                # 遷移を取り消す
                self._move_computer(del_oi, del_oj, del_i, del_j)
                self._undo_move(add_ni, add_nj, add_i, add_j, last=False)
        return

    def _move_computer(self, i, j, ni, nj):
        self.C[i][j], self.C[ni][nj] = 0, self.C[i][j]
        self.moves.append((i, j, ni, nj))
        self.move_check[(i,j,ni,nj)] = 1
        self.rev_moves[(ni, nj)].append((i, j))
        self.can_remove[i][j] = 0
        self.can_remove[ni][nj] = 1
        self.in_cnt[ni][nj] += 1
        self.out_cnt[i][j] += 1

    def _undo_move(self, ni, nj, i, j, last=True):
        # (ni,nj)を(i,j)に戻す
        self.C[ni][nj], self.C[i][j] = 0, self.C[ni][nj]
        if last:
            self.moves.pop()
            self.rev_moves[(ni, nj)].pop()
        else:
            if (i,j,ni,nj) not in self.moves:
                print(i,j,ni,nj,file=sys.stderr)
                print(self.moves, self.rev_moves, file=sys.stderr)
                pass
            self.moves.remove((i, j, ni, nj))
            self.rev_moves[(ni, nj)].remove((i, j))
        self.move_check[(i,j,ni,nj)] = 0
        self.can_remove[i][j] = 1
        self.can_remove[ni][nj] = 0
        self.in_cnt[ni][nj] -= 1
        self.out_cnt[i][j] -= 1


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
        # print(v, file=sys.stderr)
        if not (1 <= C[i][j] <= K):
            print(v,C[i][j],file=sys.stderr)
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

    #判定問題の条件を満たすときTrueを返す関数
    def is_ok(target, N, K, C):
        check_solver = Solver(N, K, deepcopy(C), K*200)
        res = check_solver.solve(target)
        l = len(res.moves) + len(res.connects)
        # print(target, l, file=sys.stderr)
        # print(f"Score = {calc_score(N, K, deepcopy(C), res)}", file=sys.stderr)
        return l < K * 120

    #求めるのが最大値か最小値かでokとngが反転
    ok, ng = (high, low-1) if get_mini else (low, high+1)
    mid = (ok+ng)//2
    while abs(ok-ng)>1:
        ok, ng = (mid, ng) if is_ok(mid, N, K, C) else (ok, mid)
        mid = (ok+ng)//2
    return ok


def main():
    N, K = map(int, input().split())
    C = [list(map(int, list(input()))) for _ in range(N)]

    LIM = K*100
    # 単純に下限と上限を指定
    low, high = 0, LIM
    move_lim = binary_search(low,high,N,K,C,get_mini=False)

    TIME_LIMIT = 2.3
    solver = Solver(N, K, deepcopy(C), LIM, TIME_LIMIT)
    res = solver.solve(move_lim, hill=True)
    print(K, move_lim, len(res.moves), len(res.connects), file=sys.stderr)
    print(f"Score = {calc_score(N, K, deepcopy(C), res)}", file=sys.stderr)

    print_answer(res)


if __name__ == "__main__":
    start = time()
    main()
