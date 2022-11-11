def get_diff(degree1, degree2):
    return sum(abs(degree1[i]-degree2[i])for i in range(N))
def get_degrees(s):
    ind = 0
    matrix = [[0]*N for _ in range(N)]
    for i in range(N):
        for j in range(i+1,N):
            matrix[i][j] = matrix[j][i] = s[ind]
            ind += 1
    cnts = sorted(matrix[i].count("1")for i in range(N))
    return cnts
from random import *
from time import *
import sys
start = time()
INF = 10**18
M, eps = input().split()
M, eps = int(M),float(eps)
N = 10
print(N)
L = N*(N-1)//2
G = [[[0]*N for _ in range(N)] for _ in range(M)]
max_diff = -1
degrees = [0]*M
res = [0]*M
for _ in range(10):
    new_degrees = [0]*M
    new_res = [0]*M
    for k in range(M):
        s = "".join(choices(["0","1"],k=N*(N-1)//2))
        new_res[k] = s
        new_degrees[k] = get_degrees(s)
    diff = min(get_diff(new_degrees[i],new_degrees[j])for i in range(M)for j in range(i+1,M))
    # print("#",diff)
    if diff > max_diff:
        degrees = new_degrees
        max_diff = diff
        res = new_res
# print("#",max_diff)
for k in range(M):print(res[k])
for q in range(100):
    H = input()
    D = get_degrees(H)
    # print("#",D)
    min_diff = INF
    min_ind = -1
    for i in range(M):
        diff = get_diff(D,degrees[i])
        # print("#",i,diff)
        if diff < min_diff:
            min_diff = diff
            min_ind = i
    print(min_ind)
# print("#",time()-start,file=sys.stderr)