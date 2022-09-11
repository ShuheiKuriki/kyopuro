import sys
I = sys.stdin.readline;f=lambda:map(int,I().split())
MOD = 10**9+7
T = int(I())
ans = [""]*T
M = 3000
from collections import defaultdict
for t in range(1,T+1):
    tree_a = defaultdict(lambda: 0)
    tree_b = defaultdict(lambda: 0)
    well_x = defaultdict(lambda: 0)
    well_y = defaultdict(lambda: 0)
    for i in range(int(I())):
        a,b = f()
        tree_a[a]+=1; tree_b[b]+=1
    for i in range(int(I())):
        x,y = f()
        well_x[x]+=1; well_y[y]+=1
    res = 0
    X = list(well_x.items())
    Y = list(well_y.items())
    for a,c1 in tree_a.items():
        for x,c2 in X:
            res += (a-x)**2%MOD*c1%MOD*c2%MOD
            res %= MOD
    for b,c1 in tree_b.items():
        for y,c2 in Y:
            res += (b-y)**2%MOD*c1%MOD*c2%MOD
            res %= MOD
    ans[t-1] = f"Case #{t}: {res}"
print(*ans, sep='\n')