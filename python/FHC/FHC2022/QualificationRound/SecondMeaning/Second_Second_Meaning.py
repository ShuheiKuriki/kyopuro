from collections import *
from itertools import *
I=input;f=lambda:map(int,I().split());R=range
T = int(I())
M = 10
for t in R(1,T+1):
    N,S = int(I()),I()
    L = len(S)
    l = min(M,L)
    print(f"Case #{t}:")
    ans = []
    for bit in R(1,1<<M):
        s = "".join("." if (bit>>i)%2 else "-"for i in R(M))
        if s[:l]==S[:l]: continue
        ans.append(s)
        if len(ans)==N-1:break
    print(*ans, sep='\n')