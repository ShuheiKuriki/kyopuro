from collections import *
from itertools import *
class Graph:
    def __init__(self,arr=None,s=None):
        self.matrix = [[0]*N for _ in range(N)]
        if arr is not None:
            self.arr = arr
            self.get_matrix_and_s_from_arr()
            print(self.s)
        else:
            self.s = s
            self.get_matrix_from_s()
        self.make_first_groups()

    def get_matrix_and_s_from_arr(self):
        cum = [0]+list(accumulate(self.arr))
        for l,r in zip(cum,cum[1:]):
            for i in range(l,r):
                for j in range(i+1,r):
                    self.matrix[i][j] = self.matrix[j][i] = 1
        self.s = ''.join([str(self.matrix[i][j])for i in range(N)for j in range(i+1,N)])

    def get_matrix_from_s(self):
        ind = 0
        for i in range(N):
            for j in range(i+1,N):
                self.matrix[i][j] = self.matrix[j][i] = int(self.s[ind])
                ind += 1

    def make_first_groups(self):
        # とりあえずgroupを作る
        decided = [0]*N
        self.groups = []
        for i in range(N):
            if decided[i]: continue
            lis = [i] + [j for j in range(N) if self.matrix[i][j] and not decided[j]]
            if len(lis) <= Min*(0.45-eps/2): continue
            group = deque([])
            for j in range(N):
                if decided[j]:continue
                cnt = sum(self.matrix[j][l] for l in lis)
                if cnt >= (len(lis)-1)*(0.65-eps):
                    decided[j] = 1
                    group.append(j)
            if len(group):
                self.groups.append(group)

    def get_arr_from_groups(self):
        self.lg = len(self.groups)
        self.arr = sorted(len(self.groups[g])for g in range(self.lg)if self.groups[g])
        self.arr2 = sorted((len(self.groups[g]),g)for g in range(self.lg)if self.groups[g])
        print("#",self.arr)

    def get_diff(self, G2):
        l1,l2 = len(self.arr),len(G2.arr)
        if l1 < l2:
            arr1 = [0]*(l2-l1)+self.arr
            arr2 = G2.arr
        else:
            arr1 = self.arr
            arr2 = [0]*(l1-l2)+G2.arr
        return sum(abs(a1-a2)for a1,a2 in zip(arr1,arr2))

    def remove_zero_group(self):
        self.groups = [group for group in self.groups if len(group)]
        self.lg = len(self.groups)

    # 頂点ごとに一番結びつきが強いグループに再配置
    def arrange_group(self):
        v_to_g = [-1]*N
        lg = len(self.groups)
        new_groups = [deque([])for _ in range(lg)]
        for v in range(N):
            max_prob = 0
            for g in range(lg):
                if len(self.groups[g])<Min*(0.45-eps/2):continue
                prob = sum(self.matrix[v][u]for u in self.groups[g])/len(self.groups[g])
                if prob > max_prob:
                    v_to_g[v] = g
                    max_prob = prob
            new_groups[v_to_g[v]].append(v)
        self.groups = new_groups
        self.remove_zero_group()

    # グループ順に属する頂点を一番結びつきが強いグループに再配置
    # ただし、頂点数が不足しているグループに配置されやすくする
    def arrange_group2(self,t):
        v_to_g = [-1]*N
        self.get_arr_from_groups()
        for _, g1 in self.arr2:
            l1 = len(self.groups[g1])
            for _ in range(l1):
                v = self.groups[g1].popleft()
                max_prob = -1
                for _, g2 in self.arr2:
                    if g2 == g1 and l1 < Min*(0.5+t*0.02):continue
                    l2 = len(self.groups[g2])
                    if l2 < 2: continue
                    prob = sum(self.matrix[v][u]for u in self.groups[g2])/l2
                    if l2 < Min: prob*=1.5
                    if prob > max_prob:
                        v_to_g[v] = g2
                        max_prob = prob
                self.groups[v_to_g[v]].append(v)
        self.remove_zero_group()

    # 頂点ごとに一番結びつきが強いグループに再配置(2グループ統合用)
    def arrange_two_groups(self,groups):
        v_to_g = [-1]*N
        lg = len(groups)
        vs = groups[0]+groups[1]
        new_groups = [deque([])for _ in range(lg)]
        for v in vs:
            max_prob = -1
            for g in range(lg):
                prob = sum(self.matrix[v][u]for u in groups[g])/len(groups[g])
                if prob > max_prob:
                    v_to_g[v] = g
                    max_prob = prob
            new_groups[v_to_g[v]].append(v)
        return new_groups

    def divide_group(self):
        for g in range(self.lg):
            lis = list(self.groups[g])
            l = len(lis)
            if l <= 3: continue
            cnt = sum(self.matrix[v1][v2]for v1 in lis for v2 in lis)
            prob1 = cnt/(l*(l-1))
            print("#",prob1)
            if prob1 > 0.6: continue
            print("#","divide")
            vs = set(lis[:3])
            for i1,v1 in enumerate(lis):
                for i2,v2 in enumerate(lis[i1+1:]):
                    for v3 in lis[i2+1:]:
                        if self.matrix[v1][v2]==self.matrix[v1][v3]==self.matrix[v2][v3]==1:
                            vs = {v1,v2,v3}
                            break
                    else: continue
                    break
                else: continue
                break
            vs1,vs2 = vs,[]
            for v in lis:
                if v in vs1:continue
                prob = sum(self.matrix[v][v1]for v1 in vs1)/len(vs1)
                if prob > prob1:vs1.add(v)
                else:vs2.append(v)
            if len(vs2):
                divided_groups = [list(vs1),vs2]
                print("#",divided_groups)
                divided_groups = self.arrange_two_groups(divided_groups)
                print("#",divided_groups)
                self.groups[g] = divided_groups[0]
                self.groups.append(divided_groups[1])

    def merge_group(self):
        for g1 in range(self.lg):
            if len(self.groups[g1])==0:continue
            for g2 in range(g1+1,self.lg):
                cnt = sum(self.matrix[v1][v2]for v1 in self.groups[g1]for v2 in self.groups[g2])
                l1,l2 = len(self.groups[g1]),len(self.groups[g2])
                if l2==0:continue
                prob = cnt/(l1*l2)
                # print("#",prob)
                if prob > 0.7-eps:
                    self.groups[g1] += self.groups[g2]
                    self.groups[g2] = []
        self.remove_zero_group()

    def shape_matrix(self):
        # 頂点ごとに一番結びつきが強いグループに再配置
        self.arrange_group()
        for t in range(5):
            print("#",t)
            # グループ順に属する頂点を一番結びつきが強いグループに再配置
            # ただし、頂点数が不足しているグループに配置されやすくする
            self.arrange_group2(t)
            self.divide_group()
            self.merge_group()

def rec(lis,Sum,Min):
    if Sum==N:return[lis]
    res = []
    for i in range(Min,N-Sum+1):
        res.extend(rec(lis+[i],Sum+i,i))
    return res


M, eps = input().split()
M, eps = int(M),float(eps)
Min = 9
N = [19,24,28,33,37,41,45,48,52,56,59,63,66,69,73,76,80,83,86,89,92,96,99][Min-2]
print(N)
L = N*(N-1)//2
arrs = rec([],0,Min)
matrices = [0]*M
for k in range(M):
    G = Graph(arr=arrs[k])
    matrices[k] = G
for q in range(100):
    print("#",q)
    H = input()
    G = Graph(s=H)
    G.shape_matrix()
    lis = [G.get_diff(matrices[i])for i in range(M)]
    t = lis.index(min(lis))
    print(t)