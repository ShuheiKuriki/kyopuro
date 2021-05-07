def solve(N,A):
    ans = 0
    return ans
def gutyoku(N,A):
    ans = 0
    return ans
T = int(input())
from random import *
for t in range(T):
    N = randint(1,100)
    A = choices(range(101), k=N)
    a = solve(N,A); b = gutyoku(N,A)
    if a!=b:
        print(N)
        print(*A)
        print(a,b)

