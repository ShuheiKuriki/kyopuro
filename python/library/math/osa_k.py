from collections import defaultdict
def sieve(n):
    fact = [float('inf')]*(n+1)
    fact[1] = 1
    for i in range(2, n+1):
        if fact[i]==float('inf'):
            j = i
            while j <= n:
                fact[j] = min(fact[j], i)
                j += i
    return fact
def osa_k(n):
    fct = defaultdict(lambda: 0)
    while n>1:
        fct[facts[n]] += 1
        n //= fct[n]
    return fct
M = int(input())
facts = sieve(M)