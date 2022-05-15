import sys,os,io
input = sys.stdin.readline
#input = io.BytesIO(os.read(0,os.fstat(0).st_size)).readline
T = int(input())
ans = [0]*T
up = 1
down = 0
for t in range(1,T+1):
    S = input()[:-1]
    N = len(S)
    diff = down
    res = S[-1]
    for i in range(N-2,-1,-1):
        if S[i]<S[i+1]: diff = up
        elif S[i]>S[i+1]: diff = down
        res += S[i]
        if diff == up: res += S[i]
    res = res[::-1]      
    ans[t-1] = f"Case #{t}: {res}"
print(*ans, sep='\n')