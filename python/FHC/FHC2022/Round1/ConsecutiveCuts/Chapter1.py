import sys
I=sys.stdin.readline;f=lambda:map(int,I().split())
def solve(t,N,K,A,B):
    a = A.index(1)
    b = B.index(1)
    res = "NO"
    if A == B:
        if N == 2:
            if K % 2 == 0: res = "YES"
        else:
            if K != 1: res = "YES"
    else:
        A = A[a:] + A[:a]
        B = B[b:] + B[:b]
        if A == B:
            if N == 2:
                if K % 2 == 1: res = "YES"
            else:
                if K > 0: res = "YES"
    return f"Case #{t}: {res}"               

if __name__ == '__main__':
    T = int(I())
    ans = [""]*T
    for t in range(1,T+1):
        N,K = f()
        A,B = list(f()),list(f())
        ans[t-1] = solve(t,N,K,A,B)
    print(*ans, sep='\n')