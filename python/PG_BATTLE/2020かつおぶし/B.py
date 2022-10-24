N,S=map(int,input().split())
def dfs(n,m,s):
    if n==1:return[[s]]
    res = []
    for i in range(m,s):
        if i*n > s:break
        for lis in dfs(n-1,i,s-i):
            res.append([i]+lis)
    return res
# for n in range(1,51):
#     for s in range(n,51):
#         print(f"{n=},{s=},{len(dfs(n,1,s))}")
for lis in dfs(N,1,S):print(*lis)