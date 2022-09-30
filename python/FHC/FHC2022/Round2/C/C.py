import sys; input = sys.stdin.readline
f = lambda:map(int,input().split())
MOD = 10**9+7
def solve():
    N,K = f()
    A = [list(f()) for _ in range(N)]
    res = 0
    return res
if __name__ == '__main__':
    print(*[f"Case #{t+1}: {solve()}"for t in range(int(*f()))],sep='\n')