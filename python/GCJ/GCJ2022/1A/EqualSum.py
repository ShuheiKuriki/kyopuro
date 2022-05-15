import sys,os,io
input = sys.stdin.readline
#input = io.BytesIO(os.read(0,os.fstat(0).st_size)).readline
T = int(input())
A = set(1<<i for i in range(30))
lis2 = []
for i in range(1,1000):
    if i not in A:
        A.add(i)
        lis2.append(i)
    if len(A)==100: break
A = sorted(A)
for t in range(1,T+1):
    N = int(input())
    print(*A[:N], flush=True)
    B = list(map(int, input().split()))
    M = sum(A[:N]+B)//2
    C = sorted(lis2[:N]+B, reverse=True)
    now = 0
    ans = []
    for c in C:
        if now + c <= M:
            now += c
            ans.append(c)
        else:
            break
    rem = M - now
    for i in range(40):
        if (rem>>i)%2: ans.append(1<<i)
    print(*ans, flush=True)