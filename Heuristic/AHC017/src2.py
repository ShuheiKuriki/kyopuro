import sys;RL=sys.stdin.readline
I=lambda:map(int,RL().split())
N,M,D,K = I()
A = [tuple(I())for _ in range(M)]
ans = [0]*M
day_cnt = [0]*D
day = 0
Sets = [set()for _ in range(D)]
for i,(u,v,w) in enumerate(A):
    start = day
    while day < start+D and (day_cnt[day%D] >= K or u in Sets[day%D] or v in Sets[day%D]):
        day += 1
    day_mod = day%D
    if day==start+D:
        day_mod = day%D
        for d in range(1,D+1):
            if day_cnt[d] < K:
                Sets[d].add(u);Sets[d].add(v)
                ans[i] = d+1
                day_cnt[d] += 1
                break
    else:
        Sets[day_mod].add(u);Sets[day_mod].add(v)
        ans[i] = day_mod+1
        day_cnt[day_mod] += 1
print(*ans)