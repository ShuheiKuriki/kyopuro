from random import *
import sys
from copy import deepcopy
from itertools import permutations
from collections import defaultdict
from time import time
from math import exp
from itertools import groupby

seed(1)

class Result:

    def __init__(self, moves, connects):
        self.moves = moves
        self.connects = connects


class Solver:
    USED = -1
    di = [1, 0, -1, 0]
    dj = [0, 1, 0, -1]

    def __init__(self, N, K, C, LIM, WIDTH, start=-1, TIME_LIMIT=-1, MAX_STEP=-1, s_temp=-1, e_temp=-1):
        self.N = N
        self.K = K
        self.C = C
        self.LIM = LIM
        self.WIDTH = WIDTH
        self.moves = []
        self.rev_moves = defaultdict(lambda: [])
        self.can_remove = [[0]*N for _ in range(N)]
        self.in_cnt = [[0]*N for _ in range(N)]
        self.out_cnt = [[0]*N for _ in range(N)]
        self.move_check = defaultdict(lambda: 0)
        self.connects = []
        self.src_ord = list(range(1,K+1))
        if start >= 0: self.start = start
        if TIME_LIMIT >= 0: self.TIME_LIMIT = TIME_LIMIT
        if MAX_STEP >= 0: self.max_step = MAX_STEP
        if s_temp >= 0: self.s_temp = s_temp
        if e_temp >= 0: self.e_temp = e_temp

    def solve(self, move_lim, hill=False):

        self._move(move_lim)

        step = update = 0

        if hill: step, update = self._hill_climb()
        
        self._connect(self.LIM - len(self.moves))

        return step, update, Result(self.moves, self.connects)

    def _move(self, lim):

        def find_best():
            min_dist = 10**10
            for perm in permutations(range(self.K), r=self.K):
                lis = list(perm)
                dists = [0]*self.K
                for i in range(self.N):
                    for j in range(self.N):
                        c = self.C[i][j]
                        if c == 0: continue
                        c -= 1
                        m = lis[c]
                        dists[c] += min(abs(i % self.K - m), abs(i % self.K - (m+self.K)), abs(i % self.K - (m-self.K)))
                if sum(dists) < min_dist:
                    best_goals = lis[:]
                    min_dist = sum(dists)
                    min_dists = dists[:]
            src_ord = list(map(lambda x:x[1], sorted((d,i+1) for i,d in enumerate(min_dists))))
            return best_goals, src_ord

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

        goals, src_ord = find_best()
        self.src_ord = src_ord
        t = 0
        while t < 10:
            for c in self.src_ord:
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
                            return
            t += 1
        # print("t", t, file=sys.stderr)
        return

    def _connect(self, lim: int):

        f = lambda i,j: i*self.N+j
        rle = lambda s: [(gs[0], len(list(gs[1]))) for gs in groupby(s)]

        uf = UnionFind(self.N*self.N, self.K)

        rrle = [rle(self.C[i][j] for j in range(self.N) if 1 <= self.C[i][j] <= self.K) for i in range(self.N)]
        crle = [rle(self.C[i][j] for i in range(self.N) if 1 <= self.C[i][j] <= self.K) for j in range(self.N)]

        cnts = [0]*(self.K+1)
        for i in range(self.N):
            for k,v in rrle[i]: cnts[k] += v-1        
        for j in range(self.N):
            for k,v in crle[j]: cnts[k] += v-1
        cnts = sorted((c,i+1) for i,c in enumerate(cnts[1:]))[::-1]
        self.src_ord = [c for _,c in cnts]

        def connect_dots(i1,j1,i2,j2,c,assertion=True):
            lj, rj = min(j1,j2)+1, max(j1,j2)
            li, ri = min(i1,i2)+1, max(i1,i2)
            if assertion:
                c1, c2 = self.C[i1][j1], self.C[i2][j2]
                if c1 > self.K: c1 -= self.K
                if c2 > self.K: c2 -= self.K
                if c1 != c2 or c1 != c: raise AssertionError
                lis = self.C[i1][lj:rj] if i1 == i2 else [self.C[i][j1] for i in range(li,ri)]
                if self.USED in lis: raise AssertionError
                if uf.same(f(i1,j1), f(i2,j2)): raise AssertionError
            uf.union(f(i1,j1), f(i2,j2))
            self.connects.append((i1,j1,i2,j2))
            if i1 == i2:
                for j in range(lj,rj): self.C[i1][j] = self.USED
            else:
                for i in range(li,ri): self.C[i][j1] = self.USED

        def build_bridge(i1,j1,i2,j2,i3,j3,c):
            if len(self.connects) >= lim-1: raise AssertionError
            c1, c2, c3 = self.C[i1][j1], self.C[i2][j2], self.C[i3][j3]
            if c1 > self.K: c1 -= self.K
            if c2 > self.K: c2 -= self.K
            if c3 > self.K: c3 -= self.K
            if c1 != c or c2 in [self.USED,0,c] or c3 != c: raise AssertionError
            lis1 = self.C[i1][min(j1,j2)+1:max(j1,j2)] if i1 == i2 else [self.C[i][j1] for i in range(min(i1,i2)+1,max(i1,i2))]
            lis2 = self.C[i2][min(j2,j3)+1:max(j2,j3)] if i2 == i3 else [self.C[i][j2] for i in range(min(i2,i3)+1,max(i2,i3))]
            if self.USED in lis1 + lis2: raise AssertionError
            if uf.same(f(i1,j1), f(i2,j2)) or uf.same(f(i1,j1), f(i3,j3)): raise AssertionError
            s1, s2, s3 = uf.size(f(i1,j1)), uf.size(f(i2,j2)), uf.size(f(i3,j3))
            d1, d2, d3 = uf.get_dummy(f(i1,j1)), uf.get_dummy(f(i2,j2)), uf.get_dummy(f(i3,j3))
            n1, n2, n3 = s1-d1, s2-d2, s3-d3
            if n1*n3 > s2*(n1+n3):
                connect_dots(i1,j1,i2,j2,c,assertion=False)
                connect_dots(i2,j2,i3,j3,c,assertion=False)
                if self.C[i2][j2] <= self.K:
                    uf.set_dummy(f(i2,j2), 1)
                    self.C[i2][j2] = self.K + c

        for c in self.src_ord:
            row = [[j for j in range(self.N) if 1 <= self.C[i][j] <= self.K*2] for i in range(self.N)]
            col = [[i for i in range(self.N) if 1 <= self.C[i][j] <= self.K*2] for j in range(self.N)]

            for i in range(self.N):
                for j1,j2 in zip(row[i][:-1],row[i][1:]):
                    try:
                        connect_dots(i,j1,i,j2,c)
                    except AssertionError:
                        continue
                    if len(self.connects) == lim: return

            for j in range(self.N):
                for i1,i2 in zip(col[j][:-1],col[j][1:]):
                    try:
                        connect_dots(i1,j,i2,j,c)
                    except AssertionError:
                        continue
                    if len(self.connects) == lim: return

            for i in range(self.N):
                for j1,j2,j3 in zip(row[i][:-2],row[i][1:-1],row[i][2:]):
                    try:
                        build_bridge(i,j1,i,j2,i,j3,c)
                    except AssertionError:
                        pass
                    else:
                        if len(self.connects) == lim: return

                    ind = col[j2].index(i)

                    if ind > 0:
                        i1 = col[j2][ind-1]
                        try:
                            build_bridge(i,j1,i,j2,i1,j2,c)
                        except AssertionError:
                            pass
                        else:
                            if len(self.connects) == lim: return

                    if ind < len(col[j2]) - 1:
                        i1 = col[j2][ind+1]
                        try:
                            build_bridge(i,j1,i,j2,i1,j2,c)
                        except AssertionError:
                            pass
                        else:
                            if len(self.connects) == lim: return

            for j in range(self.N):
                for i1,i2,i3 in zip(col[j][:-2],col[j][1:-1],col[j][2:]):
                    try:
                        build_bridge(i1,j,i2,j,i3,j,c)
                    except AssertionError:
                        continue
                    else:
                        if len(self.connects) == lim: return

                    ind = row[i2].index(j)
                    if ind < len(row[i2]) - 1:
                        j1 = row[i2][ind+1]
                        try:
                            build_bridge(i1,j,i2,j,i2,j1,c)
                        except AssertionError:
                            pass
                        else:
                            if len(self.connects) == lim: return
        return

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
            width = self.WIDTH
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

        update = 0
        for step in range(self.max_step):
            if step % 100 == 0:
                now = time()-self.start
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

            temp = (self.s_temp*(self.max_step-step)+self.e_temp*step)/self.max_step
            diff = del_diff + add_diff

            if diff > 0 or (temp > 0 and exp((diff-1)/temp) > random()):
            # if diff > 0:
                # 遷移を採用する
                update += 1
            else:
                # 遷移を取り消す
                self._move_computer(del_oi, del_oj, del_i, del_j)
                self._undo_move(add_ni, add_nj, add_i, add_j, last=False)
        return step, update

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
            self.moves.remove((i, j, ni, nj))
            self.rev_moves[(ni, nj)].remove((i, j))
        self.move_check[(i,j,ni,nj)] = 0
        self.can_remove[i][j] = 1
        self.can_remove[ni][nj] = 0
        self.in_cnt[ni][nj] -= 1
        self.out_cnt[i][j] -= 1


class UnionFind():
    def __init__(self, n, k):
        self.n = n
        self.k = k
        self.parents = [-1] * n
        self.dummy = [0]*n

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
        self.dummy[x] += self.dummy[y]
        self.parents[y] = x

    def same(self, x, y):
        return self.find(x) == self.find(y)

    def size(self, x):
        return abs(self.parents[self.find(x)])

    def set_dummy(self, x, d):
        self.dummy[self.find(x)] += d

    def get_dummy(self, x):
        return self.dummy[self.find(x)]

def calc_score(N, K, C, res: Result):
    assert len(res.moves) + len(res.connects) <= K*100
    # 計算量O(10^5)
    for v in res.moves:
        i, j, ni, nj = v
        # print(v, file=sys.stderr)
        assert 1 <= C[i][j] <= K
        assert C[ni][nj] == 0
        C[ni][nj], C[i][j] = C[i][j], 0

    uf = UnionFind(N*N, K)
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


def move_lim_search(N, K, C, WIDTH):

    LIM = K*100
    best_score = 0
    for move_lim in range(K*5, LIM+1, K*5):
        search_solver = Solver(N, K, deepcopy(C), LIM, WIDTH)
        _, _, res = search_solver.solve(move_lim)
        move_l, con_l = len(res.moves), len(res.connects)
        score = calc_score(N, K, deepcopy(C), res)
        print(f"move_lim = {move_lim}, total_l = {move_l + con_l}, move_l = {move_l}, con_l = {con_l}, score = {score}", file=sys.stderr)
        if score > best_score:
            best_score = score
            best_lim = move_lim
            best_res = res
    print(file=sys.stderr)
    print(f"best_lim = {best_lim}, best_score = {best_score}", file=sys.stderr)
    print(file=sys.stderr)
    return best_lim, best_score, best_res


def main():
    N, K = map(int, input().split())
    C = [list(map(int, list(input()))) for _ in range(N)]

    LIM = K*100
    WIDTH = 5

    move_lim, search_score, search_res = move_lim_search(N,K,C,WIDTH)

    TIME_LIMIT = 2
    MAX_STEP = 100000

    hill = 3
    temps = [0.0001, 0.0004, 0.001, 0.004, 0.01, 0.04, 0.1]
    L = hill + len(temps)
    # 山登り
    hill_score = 0
    s_temp, e_temp = 0, 0
    for _ in range(hill):
        solver = Solver(N, K, deepcopy(C), LIM, WIDTH, time(), TIME_LIMIT / L, MAX_STEP, s_temp, e_temp)
        step, upd, res = solver.solve(move_lim, hill=True)
        score = calc_score(N, K, deepcopy(C), res)
        print(f"s_temp = {s_temp}, e_temp = {e_temp}, step = {step}, update = {upd}, score = {score}", file=sys.stderr)
        if score > hill_score:
            hill_score = score
            hill_res = res
    print(file=sys.stderr)

    # 焼き鈍し
    anneal_score = 0
    for temp in temps:
        s_temp, e_temp = temp*5, temp
        solver = Solver(N, K, deepcopy(C), LIM, WIDTH, time(), TIME_LIMIT / L, MAX_STEP, s_temp, e_temp)
        step, upd, res = solver.solve(move_lim, hill=True)
        score = calc_score(N, K, deepcopy(C), res)
        print(f"s_temp = {s_temp}, e_temp = {e_temp}, step = {step}, update = {upd}, score = {score}", file=sys.stderr)
        if score > anneal_score:
            anneal_score = score
            anneal_res = res

    print(file=sys.stderr)
    print(f"search_score = {search_score}, hill_score = {hill_score}, anneal_score = {anneal_score}", file=sys.stderr)

    max_score = max(search_score, hill_score, anneal_score)
    if search_score == max_score: res = search_res
    if hill_score == max_score: res = hill_res
    if anneal_score == max_score: res = anneal_res

    print(file=sys.stderr)
    print(f"src_ord = {solver.src_ord}",file=sys.stderr)
    print(f"K = {K}, move_l = {len(res.moves)}, con_l = {len(res.connects)}", file=sys.stderr)
    print(f"src_score = {max_score}", file=sys.stderr)
    print(file=sys.stderr)

    print_answer(res)


if __name__ == "__main__":
    main()
