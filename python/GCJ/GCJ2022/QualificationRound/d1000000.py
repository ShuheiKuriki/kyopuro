import sys,os,io
input = sys.stdin.readline
#input = io.BytesIO(os.read(0,os.fstat(0).st_size)).readline
T = int(input())
ans = [0]*T
for t in range(T):
    N = int(input())
    A = sorted(list(map(int, input().split())))
    ind = 0
    die = 1
    while ind < N:
        while ind < N and A[ind] < die:
            ind += 1
        if ind == N: break
        die += 1
        ind += 1
    ans[t] = f"Case #{t+1}: {die-1}"
print(*ans, sep='\n')