import sys; input = sys.stdin.readline
I = lambda:map(int,input().split())
N, Wlim = I()
n1 = N//2
n2 = N-n1
V1,V2,W1,W2 = [0]*n1,[0]*n2,[0]*n1,[0]*n2
for i in range(n1):
    V1[i],W1[i] = I()
for i in range(n2):
    V2[i],W2[i] = I()
from collections import defaultdict
from bisect import *
def make(V,W,n):
    Ws = {0}
    value = defaultdict(lambda: 0)
    for i in range(n):
        lis = sorted(Ws,reverse=True)
        for l in lis:
            Ws.add(l+W[i])
            value[l+W[i]] = max(value[l+W[i]],value[l]+V[i])
    Ws = sorted(Ws)
    for i in range(1,len(Ws)):
        value[Ws[i]] = max(value[Ws[i]], value[Ws[i-1]])
    return Ws, value
Ws1,value1 = make(V1,W1,n1)
Ws2,value2 = make(V2,W2,n2)
ans = 0
for w1 in Ws1:
    if w1>Wlim:
        break
    w2 = Ws2[bisect_right(Ws2,Wlim-w1)-1]
    ans = max(ans, value1[w1]+value2[w2])
print(ans)