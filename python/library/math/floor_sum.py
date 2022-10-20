def floor_sum(n, m, a, b):
    res = 0
    while True:
        if a >= m: #整数傾き分
            res += (n - 1) * n * (a // m) // 2
            a %= m
        if b >= m: #下の長方形の分
            res += n * (b // m)
            b %= m
        y_max = (a * n + b) // m #y座標の最大整数
        if y_max == 0: break
        # x_max : y = b/a + x * a/m と y = y_max の交点のx座標の最大値のa倍
        x_max = m * y_max - b
        # diff : nとx座標最大値の差のa倍
        diff = n * a - x_max
        res += diff // a * y_max
        n, m, a, b = y_max, a, m, diff%a
    return res

import sys; input = sys.stdin.readline
I = lambda:map(int,input().split())

T = int(input())
ans = [0]*T

for i in range(T):
    n, m, a, b = I()
    ans[i] = floor_sum(n, m, a, b)

print(*ans, sep='\n')