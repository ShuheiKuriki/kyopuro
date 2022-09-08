from collections import *
I=input;f=lambda:map(int,I().split());R=range
T = int(I())
ans = [f"Case #{t}: YES"for t in R(1,T+1)]
for t in R(1,T+1):
    N, K = f()
    if max(Counter(f()).values()) > 2 or N > 2*K: ans[t-1] = f"Case #{t}: NO"
print(*ans, sep='\n')