def get_diff(matrix1, matrix2):
    return sum(abs(matrix1[i][j]-matrix2[i][j])for i in range(N)for j in range(N)if i!=j)
def reset_permutation(matrix):
    ind = 0
    cnts = [(matrix[i].count(0),i)for i in range(N)]
    P = [0]*N
    for i,(_,ind) in enumerate(sorted(cnts)):
        P[ind] = i
    res = [[0]*N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            res[P[i]][P[j]] = matrix[i][j]
    return res
def get_matrix_from_s(s):
    matrix = [[0]*N for _ in range(N)]
    ind = 0
    for i in range(N):
        for j in range(i+1,N):
            matrix[i][j] = matrix[j][i] = int(s[ind])
            ind += 1
        # print("#",*matrix[i])
    # print("#")
    matrix = reset_permutation(matrix)
    for i in range(N):
        prev_zero = False
        for j in range(N-1):
            if j==i:continue
            if matrix[i][j]==0:
                if prev_zero:
                    for k in range(j+1,N):
                        matrix[i][k] = matrix[k][i] = 0
                elif matrix[i][j+1]==1:
                    matrix[i][j] = matrix[j][i] = 1
                prev_zero = True
        # print("#",*matrix[i])
    # print("#")
    matrix = reset_permutation(matrix)
    # for i in range(N):
        # print("#",*matrix[i])
    # print("#")
    # print("#")
    return matrix
def get_s_from_matrix(matrix):
    res = ''.join([str(matrix[i][j])for i in range(N)for j in range(i+1,N)])
    return res
# def get_degree_from_matrix(matrix):
#     return sorted(matrix[i].count(1)for i in range(N))
def make_graph(arr):
    # print("#",arr)
    matrix = [[0]*N for _ in range(N)]
    for k,a in enumerate(arr):
        for i in range(k*unit,(k+1)*unit):
            for j in range(i,a*unit):
                matrix[i][j] = matrix[j][i] = 1
    return matrix
def rec(lis,right):
    if right<=len(lis):
        return [lis+[0]*(block-len(lis))]
    res = []
    for i in range(len(lis)+1,right+1):
        res.extend(rec(lis+[i],i))
    return res


M, eps = input().split()
M, eps = int(M),float(eps)
unit = 5
block = 9
N = unit*block
print(N)
L = N*(N-1)//2
arrs = rec([],block)
la = len(arrs)
# degrees = [0]*M
matrices = [0]*M
for k in range(M):
    G = make_graph(arrs[k])
    s = get_s_from_matrix(G)
    print(s)
    # degrees[k] = get_degree_from_matrix(G)
    matrices[k] = G
    # print("#",degrees[k])
for q in range(100):
    H = input()
    # print("#",H)
    HM = get_matrix_from_s(H)
    # print("#",HM)
    # D = get_degree_from_matrix(HM)
    lis = [get_diff(HM, matrices[i])for i in range(M)]
    t = lis.index(min(lis))
    print(t)