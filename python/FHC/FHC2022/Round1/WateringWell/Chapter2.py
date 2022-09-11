import sys
I = sys.stdin.readline;f=lambda:map(int,I().split())
MOD = 10**9+7
T = int(I())
ans = [""]*T
for t in range(1,T+1):
    N = int(input())
    A,B = [0]*N,[0]*N
    for i in range(N): A[i],B[i] = f()
    a1,b1 = sum(A)%MOD, sum(B)%MOD
    a2,b2 = sum(a*a for a in A)%MOD, sum(b*b for b in B)%MOD

    Q = int(input())
    X,Y = [0]*Q,[0]*Q
    for i in range(Q): X[i],Y[i] = f()
    x1,y1 = sum(X)%MOD, sum(Y)%MOD
    x2,y2 = sum(x*x for x in X)%MOD, sum(y*y for y in Y)%MOD

    res = Q*(a2+b2)+N*(x2+y2)-2*(a1*x1+b1*y1)
    ans[t-1] = f"Case #{t}: {res%MOD}"
print(*ans, sep='\n')