def get_diff(matrix1, matrix2):
    return sum(abs(matrix1[i][j]-matrix2[i][j])for i in range(N)for j in range(N))
def get_matrix(s):
    ind = 0
    matrix = [[0]*N for _ in range(N)]
    cnts = [0]*N
    for i in range(N):
        for j in range(i+1,N):
            matrix[i][j] = matrix[j][i] = int(s[ind])
            ind += 1
        cnts[i] = (matrix[i].count(1),i)
    P = [0]*N
    for i,(_,ind) in enumerate(sorted(cnts)):
        P[ind] = i
    res = [[0]*N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            res[P[i]][P[j]] = matrix[i][j]
    return res
from random import *
from time import *
# import sys
start = time()
INF = 10**18
M, eps = input().split()
M, eps = int(M),float(eps)
N = 15
print(N)
L = N*(N-1)//2
max_diff = -1
matrix = [[[0]*N for _ in range(N)]for _ in range(M)]
for k in range(M):
    s = "".join(choices(["0","1"],k=N*(N-1)//2))
    matrix[k] = get_matrix(s)
    print(s)
for q in range(100):
    H = input()
    Ma = get_matrix(H)
    # print("#",D)
    min_diff = INF
    min_ind = -1
    for i in range(M):
        diff = get_diff(Ma,matrix[i])
        # print("#",i,diff)
        if diff < min_diff:
            min_diff = diff
            min_ind = i
    print(min_ind)
# print("#",time()-start,file=sys.stderr)