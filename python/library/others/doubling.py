N, K = map(int, input().split())
sup = 10**18
db = [[0]*N for _ in range(sup.bit_length())]
# db[0] =  初期化
for i in range(1,sup.bit_length()):
    for j in range(N):
        db[i][j] = db[i-1][db[i-1][j]]
ans = p = 0
while K:
    if K%2:
        ans = db[p][ans]
    p += 1
    K >>= 1