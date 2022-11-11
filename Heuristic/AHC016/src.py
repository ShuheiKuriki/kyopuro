def get_diff(degree1, degree2):
    return sum(abs(degree1[i]-degree2[i])for i in range(N))
def get_degrees(s):
    ind = 0
    matrix = [[0]*N for _ in range(N)]
    for i in range(N):
        for j in range(i+1,N):
            matrix[i][j] = matrix[j][i] = s[ind]
            ind += 1
    cnts = sorted(matrix[i].count("1")for i in range(N))
    return cnts
M, eps = input().split()
M, eps = int(M),float(eps)
N = 15
print(N)
L = N*(N-1)//2
p,r = divmod(L,M)
now = 0
degrees = [0]*M
for k in range(M):
    s = "1" * now + "0" * (L-now)
    print(s)
    degrees[k] = get_degrees(s)
    now += p
    if k < r: now += 1
for q in range(100):
    H = input()
    D = get_degrees(H)
    lis = [get_diff(D, degrees[i])for i in range(M)]
    t = lis.index(min(lis))
    print(t)