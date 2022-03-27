from itertools import combinations
H, W = map(int, input().split())
A = [list(map(int, input().split())) for _ in range(H)]
cum = [[0]*(W+1) for _ in range(H+1)]
for i in range(1,H+1):
    for j in range(1,W+1):
        cum[i][j]=cum[i-1][j]+cum[i][j-1]-cum[i-1][j-1]+A[i-1][j-1]
ans = 0
for i,j in combinations(range(1,H+1),2):
    for k,l in combinations(range(1,W+1),2):
        cost = cum[j][l]+cum[i-1][k-1]-cum[j][k-1]-cum[i-1][l]
        ans = max(cost,ans)
print(ans)