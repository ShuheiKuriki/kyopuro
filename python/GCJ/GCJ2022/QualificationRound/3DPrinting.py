import sys,os,io
input = sys.stdin.readline
#input = io.BytesIO(os.read(0,os.fstat(0).st_size)).readline
T = int(input())
ans = [0]*T
for t in range(1,T+1):
    A = [list(map(int, input().split())) for _ in range(3)]
    rem = 1000000
    lis = [0]*4
    for i in range(4):
        lis[i] = min([rem, A[0][i], A[1][i], A[2][i]])
        rem -= lis[i]
    if rem>0:
        ans[t-1] = f"Case #{t}: IMPOSSIBLE"
    else:
        ans[t-1] = f"Case #{t}: {lis[0]} {lis[1]} {lis[2]} {lis[3]}"
print(*ans, sep='\n')