import cmath
pi = cmath.pi
exp = cmath.exp

# このFFTに与えるNは2**kにする
# 順変換・逆変換に与えるlistのサイズもNにする
def make_exp_t(N, base):
    exp_t = {0: 1}
    temp = N
    while temp:
        exp_t[temp] = exp(base / temp)
        temp >>= 1
    return exp_t

def fft_dfs(f, s, N, st, exp_t):
    if N==2:
        a = f[s]; b = f[s+st]
        return [a+b, a-b]
    N2 = N//2; st2 = st*2
    F0 = fft_dfs(f, s   , N2, st2, exp_t)
    F1 = fft_dfs(f, s+st, N2, st2, exp_t)
    w = exp_t[N]; wk = 1.0
    for k in range(N2):
        U = F0[k]; V = wk * F1[k]
        F0[k] = U + V
        F1[k] = U - V
        wk *= w
    F0.extend(F1)
    return F0

def fft(f, N):
    return f if N==1 else fft_dfs(f, 0, N, 1, fft_exp_t)

def ifft(F, N):
    if N==1: return F
    f = fft_dfs(F, 0, N, 1, ifft_exp_t)
    for i in range(N):
        f[i] /= N
    return f

import sys;RL=sys.stdin.readline;I=lambda:map(int,RL().split())

n = int(*I())
f = []
g = []
for i in range(n):
    a, b = map(float, input().split())
    f.append(a); g.append(b)


N = 2**(2*n-1).bit_length()
fft_exp_t = make_exp_t(N, -2j*pi)
ifft_exp_t = make_exp_t(N, 2j*pi)

f.extend([0]*(N-n))
g.extend([0]*(N-n))

F = fft(f, N)
G = fft(g, N)

FG = [F[k]*G[k] for k in range(N)]

fg = ifft(FG, N)

print(0)
for i in range(2*n-1):
    print(int(fg[i].real+0.5))