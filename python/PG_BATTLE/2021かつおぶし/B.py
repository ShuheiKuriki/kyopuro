import sys; input = sys.stdin.readline
I = lambda:map(int,input().split())
N,S = I()
D = list(I())
ans = [10**(d-1)for d in D]
Min = sum(ans)
Max = Min*10-N
if not Min<=S<=Max:exit(print(-1))
sup = [9*10**(d-1)-1 for d in D]
diff = S-Min
for i in range(N):
    m = min(diff,sup[i])
    ans[i] += m
    diff -= m
print(*ans)