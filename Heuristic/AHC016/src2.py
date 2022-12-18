from collections import*
from itertools import*
from random import*
from math import exp
from operator import xor,and_
from functools import reduce
from time import time
from heapq import*
import sys

def popcount(x):
    x = (x & 0x5555555555555555) + (x >> 1 & 0x5555555555555555)
    x = (x & 0x3333333333333333) + (x >> 2 & 0x3333333333333333)
    x = x + (x >> 4) & 0x0f0f0f0f0f0f0f0f
    x += x >> 8
    x += x >> 16
    x += x >> 32
    return x & 0x7f

def generateArray(total,min_dist,need_size,min_group_size):
    arrs = []
    for group_size in range(1,total//min_group_size+1):
        res = bfs(total,group_size,min_dist,min_group_size)
        if len(arrs)+len(res)<need_size:
            arrs.extend(res)
        else:
            shuffle(res)
            for r in res:
                arrs.append(r)
            return arrs
    return arrs

def bfs(total,num,min_dist,min_group_size):
    dists = defaultdict(lambda:min_dist+1)
    arr1 = [total//num]*(num-1) + [total//num+total%num]
    que = [(0,arr1)]
    dists[tuple(arr1)] = 0
    res = [arr1]
    while len(que):
        dist,arr1 = heappop(que)
        for i in range(num):
            for j in range(num):
                if i==j:continue
                if arr1[i]<=min_group_size:continue
                arr2 = arr1[:]
                arr2[i] -= 1
                arr2[j] += 1
                tup = tuple(sorted(arr2))
                ndist = dist+1
                for arr in res:
                    ndist = min(ndist,get_diff(arr,list(tup))//2)
                if ndist==0:continue
                ndist %= min_dist
                if ndist >= dists[tup]:continue
                if ndist == 0:
                    res.append(list(tup))
                dists[tup] = ndist
                heappush(que,(dists[tup],list(tup)))
    return res

def get_diff(arr1=None, arr2=None, G1=None, G2=None):
    if G1:arr1 = G1.best_arr
    if G2:arr2 = G2.best_arr
    l1,l2 = len(arr1),len(arr2)
    if l1 < l2:
        arr1 = [0]*(l2-l1)+arr1
    else:
        arr2 = [0]*(l1-l2)+arr2
    return sum(abs(a1-a2)for a1,a2 in zip(arr1,arr2))

def get_multinomial_table():
    p = eps/100
    prob = [[1]*(n+1)for n in range(N*N+1)]
    calc_t = time()
    inf = 1e-30
    for n in range(1,N*N+1):
        prob[n][0] = prob[n-1][0]*(1-p)
        prob[n][n] = prob[n-1][n-1]*p
        prob[n][1:n] = [prob[n-1][k-1]*p+prob[n-1][k]*(1-p)for k in range(1,n)]
        prob[n] = [0 if p < inf else p for p in prob[n]]
    print("#",time()-calc_t,file=sys.stderr)
    return prob

def add_prob(p1,p2):
    return max(SMALL,p1)*max(SMALL,p2)
def add_multi_prob(P):
    res = 1
    for p in P:
        res *= max(SMALL,p)
    return res

class Graph:
    def __init__(self,arr=None):
        self.matrix1 = [0]*N
        if N > BIT_MAX: self.matrix2 = [0]*N
        self.best_prob = -1
        self.best_arr = []
        if arr is not None:
            self.arr = arr
            self.best_arr = arr[:]
            self.get_matrix_and_s_from_arr()
            print(self.s)
        else:
            self.s = input()
            self.get_matrix_from_s()
            self.groups = [{v}for v in range(N)]
            self.v_to_g = list(range(N))
            self.get_arr_from_groups()

    def get_element(self,i,j):
        return (self.matrix1[i]>>j)%2 if j<BIT_MAX else (self.matrix2[i]>>(j-BIT_MAX))%2

    def add_element(self,i,j):
        if j<BIT_MAX: self.matrix1[i]^=1<<j
        else: self.matrix2[i]^=1<<(j-BIT_MAX)

    def get_matrix_and_s_from_arr(self):
        cum = [0]+list(accumulate(self.arr))
        for l,r in zip(cum,cum[1:]):
            for i in range(l,r):
                for j in range(i+1,r):
                    self.add_element(i,j)
                    self.add_element(j,i)
        self.s = ''.join([str(self.get_element(i,j))for i in range(N)for j in range(i+1,N)])

    def get_matrix_from_s(self):
        ind = 0
        for i in range(N):
            for j in range(i+1,N):
                if int(self.s[ind]):
                    self.add_element(i,j)
                    self.add_element(j,i)
                ind += 1

    def get_arr_from_groups(self):
        lg = len(self.groups)
        self.arr = sorted(len(self.groups[g])for g in range(lg)if self.groups[g])
        print("#",self.arr)
        print("#",[self.get_prob_of_group(g)for g in range(lg)])
        prob = add_multi_prob(self.get_prob_of_group(g)for g in range(lg))
        print(f"# prob = {prob}")
        if prob > self.best_prob:
            self.best_prob = prob
            self.best_arr = self.arr[:]

    def get_prob_of_group(self,g,group=None):
        if group is None: group = self.groups[g]
        l = len(group)
        if l==0: return 1
        if N<=BIT_MAX:
            in_bit = reduce(xor,[1<<u for u in group],0)
            in_cnt = sum(popcount(in_bit&self.matrix1[v])for v in group)
            out_bit = ((1<<N)-1)^in_bit
            out_cnt = sum(popcount(out_bit&self.matrix1[v])for v in group)
        else:
            in_bit1 = in_bit2 = 0
            for u in group:
                if u < BIT_MAX:in_bit1 ^= 1<<u
                else:in_bit2 ^= 1<<(u-BIT_MAX)
            out_bit1 = ((1<<BIT_MAX)-1)^in_bit1
            out_bit2 = ((1<<(N-BIT_MAX))-1)^in_bit2
            in_cnt1 = sum(popcount(in_bit1&self.matrix1[v])for v in group)
            in_cnt2 = sum(popcount(in_bit2&self.matrix2[v])for v in group)
            in_cnt = in_cnt1 + in_cnt2
            out_cnt1 = sum(popcount(out_bit1&self.matrix1[v])for v in group)
            out_cnt2 = sum(popcount(out_bit2&self.matrix2[v])for v in group)
            out_cnt = out_cnt1 + out_cnt2
        in_prob = MULTINOMIAL_PROB[l*(l-1)][-in_cnt-1]
        out_prob = MULTINOMIAL_PROB[l*(N-l)][out_cnt]
        prob = add_prob(in_prob,out_prob)*PROB_COEFFICIENTS[l]
        return prob

    def get_prob_of_v_and_g(self,v,g,group=None):
        if group is None: group = self.groups[g]
        l = len(group)
        in_group_flg = v in group
        if N<=BIT_MAX:
            in_bit = reduce(xor,[1<<u for u in group],0)
            in_cnt = popcount(in_bit&self.matrix1[v])
            out_bit = ((1<<N)-1)^in_bit
            out_cnt = popcount(out_bit&self.matrix1[v])
        else:
            in_bit1 = in_bit2 = 0
            for u in group:
                if u < BIT_MAX:in_bit1 ^= 1<<u
                else:in_bit2 ^= 1<<(u-BIT_MAX)
            out_bit1 = ((1<<BIT_MAX)-1)^in_bit1
            out_bit2 = ((1<<(N-BIT_MAX))-1)^in_bit2
            in_cnt = popcount(in_bit1&self.matrix1[v]) + popcount(in_bit2&self.matrix2[v])
            out_cnt = popcount(out_bit1&self.matrix1[v]) + popcount(out_bit2&self.matrix2[v])
        in_prob = MULTINOMIAL_PROB[l-in_group_flg][-in_cnt-1]
        out_prob = MULTINOMIAL_PROB[N-l-(1^in_group_flg)][out_cnt]
        prob = add_prob(in_prob,out_prob)
        return prob

    def reset_group(self):
        self.groups = [group for group in self.groups if len(group)]
        for i,group in enumerate(self.groups):
            for v in group:
                self.v_to_g[v] = i
 
    # 頂点ごとに一番結びつきが強いグループに再配置
    def arrange_group(self):
        lg = len(self.groups)
        for v in range(N):
            pre_g = self.v_to_g[v]
            max_prob = -1
            for g in range(lg):
                prob = self.get_prob_of_v_and_g(v,g)
                if prob > max_prob or (prob==max_prob and randint(0,1)):
                    self.v_to_g[v] = g
                    max_prob = prob
            self.groups[pre_g].discard(v)
            self.groups[self.v_to_g[v]].add(v)
        self.reset_group()

    # ランダムに選んだ頂点を一番結びつきが強いグループに移動させる
    def move(self,t):
        v = randint(0,N-1)
        g1 = self.v_to_g[v]
        lg = len(self.groups)
        l1 = len(self.groups[g1])
        score1 = self.get_prob_of_v_and_g(v,g1)
        score2 = -1
        move_to = -1
        for g2 in range(lg):
            if g2==g1:continue
            l2 = len(self.groups[g2])
            if l2==0:continue
            score = self.get_prob_of_v_and_g(v,g2)
            if score > score2:
                move_to = g2
                score2 = score
        if move_to == -1: return
        temp = ((LOOP-1-t)*START_TEMP_FOR_MOVE + t*END_TEMP_FOR_MOVE) / (LOOP-1)
        if score1 > 0:
            diff = (score2 - score1) / score1
        else:
            diff = 1
        if adopt(diff, temp):
            print(f"# move {diff}")
            self.v_to_g[v] = move_to
            self.groups[g1].discard(v)
            self.groups[move_to].add(v)

    def divide_group(self,t):
        # 頂点ごとに一番結びつきが強いグループに再配置(2グループ統合用)
        def arrange_two_groups(group1,group2):
            v_to_g = [-1]*N
            vs = group1|group2
            new_groups = [set(),set()]
            for v in vs:
                best_score = -1
                for g in range(2):
                    score = self.get_prob_of_v_and_g(v,g=-1,group=[group1,group2][g])
                    if score > best_score:
                        v_to_g[v] = g
                        best_score = score
                new_groups[v_to_g[v]].add(v)
            return new_groups
        def divide_small_group(g,score1):
            group = list(self.groups[g])
            l = len(group)
            res1,res2 = set(group),set()
            best_score = score1
            for bit in range(0,(1<<(l-1))-1):
                vs1,vs2 = {group[0]},set()
                for i in range(l-1):
                    if (bit>>i)%2:vs1.add(group[i+1])
                    else:vs2.add(group[i+1])
                new_score = self.get_prob_of_group(g=-1,group=vs1)*self.get_prob_of_group(g=-1,group=vs2)
                if new_score > best_score:
                    best_score = new_score
                    res1,res2 = vs1,vs2
            return res1,res2
        lg = len(self.groups)
        temp = ((LOOP-1-t)*START_TEMP_FOR_DIVIDE + t*END_TEMP_FOR_DIVIDE) / (LOOP-1)
        for g in range(lg):
            lis = list(self.groups[g])
            l = len(lis)
            if l <= 1:
                continue
            elif l <= MAX_BITSERCH_SIZE:
                score1 = self.get_prob_of_group(g=-1,group=self.groups[g])
                vs1, vs2 = divide_small_group(g,score1)
                if len(vs2):
                    self.groups[g] = vs1
                    self.groups.append(vs2)
            else:
                old_score = self.get_prob_of_group(g)
                lis2 = lis[:]
                shuffle(lis2)
                vs1,vs2 = {lis2[0]},{lis2[1]}
                for i1,v1 in enumerate(lis):
                    for i2,v2 in enumerate(lis[i1+1:]):
                        if self.get_element(v1,v2)==0: continue
                        for v3 in lis[i2+1:]:
                            if self.get_element(v1,v3)==self.get_element(v2,v3)==1:
                                vs1,vs2 = {v1,v2,v3},set()
                                break
                        else: continue
                        break
                    else: continue
                    break
                for v in lis:
                    if v in vs1:continue
                    score1 = self.get_prob_of_v_and_g(v,g=-1,group=vs1)
                    if len(vs2)>=1:
                        score2 = self.get_prob_of_v_and_g(v,g=-1,group=vs2)
                        if score1 > score2:
                            vs1.add(v)
                        else:
                            vs2.add(v)
                    else:
                        if randint(0,1):
                            vs1.add(v)
                        else:
                            vs2.add(v)
                if len(vs2):
                    # print("#",vs1,vs2)
                    divided_groups = arrange_two_groups(vs1,vs2)
                    # print("#",divided_groups)
                    new_score = add_multi_prob([self.get_prob_of_group(g=-1,group=divided_groups[i])for i in range(2)])
                    # print("# divide_new_score",new_score)
                    if old_score > 0:
                        diff = (new_score - old_score) / old_score
                    else:
                        diff = 1
                    # print("# divide_diff",diff)
                    if adopt(diff, temp):
                        print(f"# divide {diff} " \
                            f"element: {len(divided_groups[0])}+{len(divided_groups[1])}")
                        self.groups[g] = divided_groups[0]
                        self.groups.append(divided_groups[1])
        self.reset_group()

    def merge_group(self,t):
        lg = len(self.groups)
        temp = ((LOOP-1-t)*START_TEMP_FOR_MERGE + t*END_TEMP_FOR_MERGE) / (LOOP-1)
        for _ in range(lg-1):
            g1 = randint(0,lg-1)
            l1 = len(self.groups[g1])
            if l1==0:continue
            score1 = self.get_prob_of_group(g1)
            max_diff_score = -1
            merge_g = -1
            for g2 in range(lg):
                l2 = len(self.groups[g2])
                if g2==g1 or l2==0: continue
                score2 = self.get_prob_of_group(g2)
                old_score = add_prob(score1,score2)
                new_score = self.get_prob_of_group(-1, group=self.groups[g1]|self.groups[g2])
                print("#",len(self.groups[g1]),len(self.groups[g2]),old_score,new_score)
                if old_score > 0 and (new_score - old_score) / old_score > max_diff_score:
                    max_diff_score = (new_score - old_score) / old_score
                    merge_g = g2
            if merge_g == -1: continue
            # print("# merge_diff",max_diff_score)
            if adopt(max_diff_score, temp):
                print(f"# merge {max_diff_score} element: {len(self.groups[g1])}+{len(self.groups[merge_g])}")
                self.groups[g1] |= self.groups[merge_g]
                self.groups[merge_g] = set()
        self.reset_group()

    def recover_graph(self):
        for r in range(REPEAT_NUM):
            self.groups = [{v}for v in range(N)]
            self.v_to_g = list(range(N))
            for t in range(LOOP):
                print(f"# t = {t}")
                # 頂点ごとに一番結びつきが強いグループに再配置
                self.arrange_group()
                self.get_arr_from_groups()
                for _ in range(MOVE_NUM(t)):
                    self.move(t)
                self.get_arr_from_groups()
                for _ in range(DIVIDE_NUM):
                    self.divide_group(t)
                    self.get_arr_from_groups()
                for _ in range(MERGE_NUM):
                    self.merge_group(t)
                    self.get_arr_from_groups()
                print("#",t,time()-start)
        print(f"# best = {self.best_prob}, {self.best_arr}")

if __name__ == '__main__':
    start = time()
    M, eps = input().split()
    print(f"M = {M}, eps = {eps}",file=sys.stderr)
    M, eps = int(M),round(float(eps)*100)

    # MIN_DISTを決定
    DIC_FOR_MIN_DIST = {(0,22):1,(22,28):1,(28,41):3}
    MIN_DISTS = [0]*41
    for (l,r),m in DIC_FOR_MIN_DIST.items():
        MIN_DISTS[l:r] = [m]*(r-l)
    MIN_DIST = MIN_DISTS[eps]

    # Nを決定
    lis = [50,40,25]
    if eps >= 38 and M > lis[eps-38]:
        MIN,N = 1,4
    else:
        MINS = [0]*41
        MIN_FROM_EPS_AND_M = [
            [1]*101, #eps=0
            [2]*101, #eps=0.01
            [2]*101, #eps=0.02
            [2]*61+[3]*40, #eps=0.03
            [2]*41+[3]*60, #eps=0.04
            [3]*101, #eps=0.05
            [3]*101, #eps=0.06
            [3]*101, #eps=0.07
            [3]*41+[4]*60, #eps=0.08
            [3]*21+[4]*75, #eps=0.09
            [4]*21+[5]*80, #eps=0.1
            [4]*51+[5]*50, #eps=0.11
            [5]*101, #eps=0.12
            [5]*51+[6]*50, #eps=0.13
            [5]*41+[6]*60, #eps=0.14
            [6]*41+[7]*60, #eps=0.15
            [7]*71+[8]*30, #eps=0.16
            [8]*51+[9]*50, #eps=0.17
            [8]*31+[9]*40+[10]*30, #eps=0.18
            [9]*21+[10]*80, #eps=0.19
            [10]*101, #eps=0.2
            [10]*51+[11]*50, #eps=0.21
            # ここからmin_dist=3
            [8]*41+[9]*60, #eps=0.22
            [9]*41+[10]*60, #eps=0.23
            [9]*41+[10]*35+[11]*35, #eps=0.24
            [8]*21+[9]*20+[10]*20+[11]*40, #eps=0.25
            [13]*61+[14]*40, #eps=0.26
            [14]*41+[15]*45+[16]*15, #eps=0.27
            [14]*41+[15]*30+[16]*30, #eps=0.28
            [16]*21+[17]*50+[18]*30, #eps=0.29
            [20]*41+[-1]*30+[-2]*30, #eps=0.3
            [22]*41+[-1]*30+[-2]*30, #eps=0.31
            [24]*36+[-1]*50+[-2]*30, #eps=0.32
            [26]*31+[-1]*50+[-2]*30, #eps=0.33
            [28]*21+[-1]*50+[-2]*30, #eps=0.34
            [-1]*81+[-2]*20, #eps=0.35
            [-1]*81+[-2]*20, #eps=0.36
            [-1]*101, #eps=0.37
            [-1]*101, #eps=0.38
            [-1]*101, #eps=0.39
            [-1]*101 #eps=0.4
        ]
        MIN = MIN_FROM_EPS_AND_M[eps][M]
        N = 100
        if MIN < 0:
            if MIN == -2:
                MIN_DIST = 1
            for m in range(31,10,-1):
                if len(generateArray(100,MIN_DIST,M,m))>=M:
                    MIN = m
                    break
        for n in range(4,101):
            if len(generateArray(n,MIN_DIST,M,MIN))>=M:
                N = n; break

    # グローバル変数
    adopt = lambda diff,temp: diff >= 0 or (temp>0 and exp(diff/temp)) > random()
    PROB_COEFFICIENTS = [pow(min(1,(l/MIN)),10)for l in range(N+1)]
    LOOP = 20
    REPEAT_NUM = 1
    ANNEALING = 0.05
    START_TEMP_FOR_MOVE, END_TEMP_FOR_MOVE = ANNEALING, 0
    START_TEMP_FOR_DIVIDE, END_TEMP_FOR_DIVIDE = ANNEALING, 0
    START_TEMP_FOR_MERGE, END_TEMP_FOR_MERGE = ANNEALING, 0
    MOVE_NUM = lambda t: (LOOP-1-t)*5
    DIVIDE_NUM = MERGE_NUM = 2
    if MIN <= 3: DIVIDE_NUM = MERGE_NUM = 4
    EXCHANGE_LOOP = 0
    START_TEMP_FOR_EXCHANGE,END_TEMP_FOR_EXCHANGE = 0,0
    DICT_FOR_MAX_BITSEARCH_SIZE = {(0,1):13,(1,10):10,(10,41):4}
    MAX_BITSERCH_SIZES = [0]*41
    for (l,r),v in DICT_FOR_MAX_BITSEARCH_SIZE.items():
        MAX_BITSERCH_SIZES[l:r] = [v]*(r-l)
    MAX_BITSERCH_SIZE = MAX_BITSERCH_SIZES[eps]
    BIT_MAX = 50
    SMALL = 0.01 if eps == 0 else 0
    MULTINOMIAL_PROB = get_multinomial_table()
    # for n in range(N*N+1):
    #     print("#",n,MULTINOMIAL_PROB[n])

    # メイン処理
    print(f"MIN = {MIN}",file=sys.stderr)
    print(N)
    for m in range(MIN_DIST,0,-1):
        arrs = generateArray(N,m,M,MIN)
        if len(arrs)>=M:
            print(f"min_dist = {m}: arr_num = {len(arrs)}", file=sys.stderr)
            break
    arrs = [list(arr)for arr in arrs]
    graphs = [0]*M
    total = len(arrs)
    for k in range(M):
        arr = arrs[k] if total > M else arrs[k%total]
        print("#",k,arr)
        graphs[k] = Graph(arr)
    for q in range(100):
        print(f"# q = {q}")
        G = Graph()
        G.recover_graph()
        lis = [get_diff(G1=G,G2=graphs[i])for i in range(M)]
        t = lis.index(min(lis))
        print(t)
    print("time =",time()-start,file=sys.stderr)