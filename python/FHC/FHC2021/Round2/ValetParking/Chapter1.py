import sys; input = sys.stdin.readline
f = lambda:map(int,input().split())
def solve():
    R,C,K = f()
    up,down = K,R-K+1
    G = [input()[:-1]for _ in range(R)]
    score = [[0]*C for _ in range(R*3)]
    for c in range(C):
        lis = []
        for r in range(R):
            if G[r][c]=="X":lis.append(r+R)
        if len(lis)>=up:
            u = lis[up-1]
            for i in range(u,R*3):score[i][c]|=1
        if len(lis)>=down:
            d = lis[-down]
            for i in range(d+1):score[i][c]|=1
        for r in lis:score[r][c]|=1
    return min(sum(score[r][c]for c in range(C))+abs(K-1+R-r)for r in range(R*3))

if __name__ == '__main__':
    print(*[f"Case #{t+1}: {solve()}"for t in range(int(*f()))],sep='\n')