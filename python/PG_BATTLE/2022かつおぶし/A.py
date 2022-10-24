import sys; input = sys.stdin.readline
I = lambda:map(int,input().split())
N = int(*I())
A = sorted(I())
B = [A[i+1]-A[i]for i in range(N-1)]
ind = B.index(max(B))
print((A[ind]+A[ind+1])//2)