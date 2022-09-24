import sys; input = sys.stdin.readline
f = lambda:map(int,input().split())
from collections import Counter
def solve():
    N,_ = f()
    S = list(f())
    P = [Counter(f()) for _ in range(N)]
    C1 = Counter(S)
    first = Counter(S)
    Min = Counter(S)
    res = 0
    for i in range(N):
        C2 = P[i]
        for k in Min:
            Min[k] = min(Min[k], C2[k])
        cnt = 0
        for k in set(C1.keys())|set(C2.keys()):
            cnt += abs(C1[k]-C2[k])
        res += cnt//2
        C1 = C2
    for k,v in first.items():
        if Min[k]==0:res-=v
        else:
            res-=v-Min[k]
            cnt = 0
            now = v
            for i in range(N-1):
                cnt += max(0,P[i][k]-now)
                now = P[i][k]
            res-=min(Min[k],cnt)
    return max(0,res)   

if __name__ == '__main__':
    print(*[f"Case #{t+1}: {solve()}"for t in range(int(*f()))],sep='\n')