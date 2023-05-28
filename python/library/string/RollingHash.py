# 1-dimension Rolling Hash
# 参考 https://tjkendev.github.io/procon-library/python/string/rolling_hash.html
class RollingHash():
    def __init__(self, s, base, mod):
        self.mod = mod
        self.pw = pw = [1]*(len(s)+1)
        self.length = l = len(s)
        self.h = h = [0]*(l+1)
        v = 0
        for i in range(l): h[i+1] = v = (v * base + ord(s[i])) % mod
        v = 1
        for i in range(l): pw[i+1] = v = v * base % mod

    def get(self, l, r):
        # 閉区間[l,r]
        return (self.h[r] - self.h[l-1] * self.pw[r-l+1]) % self.mod
    
    def all(self):
        return self.get(0, self.length)

import sys;RL=sys.stdin.readline;I=lambda:map(int,RL().split())
base = 10**9+7; mod = (1<<61)-1
N = int(*I())
S = input()[:-1]
RHS = RollingHash(S,base,mod)