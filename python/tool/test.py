def solve(N,A):
    ans = 0
    return ans
def gutyoku(N,A):
    ans = 0
    return ans
mode = 'check'
# mode = 'experiment'
T = int(input())
from random import *
for t in range(T):
    N = 10
    A = choices(range(101), k=N)
    if mode == 'check':
        ac = gutyoku(N,A)
        sol = solve(N,A)
        if ac!=sol:
            print(f"{N=},{A=}")
            print(f"{ac=},{sol=}")
    elif mode == 'experiment':
        ac = gutyoku(N,A)
        print(f"{N=},{A=},{ac=}")
