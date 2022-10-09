import sys; input = sys.stdin.readline
f = lambda:map(int,input().split())
# LIS（最長増加部分列DP）
from bisect import bisect_left
def get_LIS(A):
    lis = []
    for i in range(N):
        ind = bisect_left(lis,A[i])
        if ind == len(lis):
            lis.append(A[i])
        else:
            lis[ind] = A[i]
    return len(lis)

N = int(input())
A = list(f())
ans = get_LIS(A)