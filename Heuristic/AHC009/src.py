from collections import deque
si, sj, ti, tj, p = input().split()
si, sj, ti, tj, p = int(si), int(sj), int(ti), int(tj), float(p)
H = [input() for _ in range(20)]
V = [input() for _ in range(19)]
dir = "ULDR"
di = [-1,0,1,0]
dj = [0,-1,0,1]
I=J=20
def is_blocked(k,i,j,ii,jj):
    if not (0<=ii<I and 0<=jj<J): return True
    if k==0 and V[i-1][j]=="1": return True #U
    if k==1 and H[i][j-1]=="1": return True #L
    if k==2 and V[i][j]=="1": return True #D
    if k==3 and H[i][j]=="1": return True #R
from random import *
def choose_dir(lis):
    m = min(a for a in lis if a>=0)
    prob = [0]*4
    for i in range(4):
        if lis[i]==-1:continue
        prob[i] = 1/(lis[i]-m+1)**2
    total = sum(prob)
    prob = [0]+[a/total for a in prob]
    for i in range(4):
        prob[i+1] += prob[i]
    r = random()
    for i in range(4):
        if prob[i]<=r<=prob[i+1]: return i
# move = 2 if p>1/3 else 1
move = 1
from collections import deque
next = [[[-1]*4 for _ in range(J)] for _ in range(I)]
que = deque([(ti,tj,0)])
next[ti][tj] = [0]*4
while len(que):
    ai,aj,cnt = que.popleft()
    for k in range(4):
        bi,bj = ai+di[k],aj+dj[k]
        if is_blocked(k,ai,aj,bi,bj): continue
        if next[bi][bj][(k+2)%4]==-1:
            next[bi][bj][(k+2)%4] = cnt+1     
            que.append((bi,bj,cnt+1)) 

prob = [[[0]*J for _ in range(I)] for _ in range(201)]
max_i = [-1]*201
max_j = [-1]*201
max_p = [0]*201
dir_bunpu = [[0]*4 for _ in range(201)]
prob[0][si][sj] = 1
ans = ""
for t in range(200//move):
    for i in range(I):
        for j in range(J):
            if (i,j) == (ti,tj): continue
            # dir_bunpu[t][choose_dir(next[i][j])] += prob[t][i][j]
            if prob[t][i][j] > max_p[t]:
                max_i[t],max_j[t],max_p[t] = i,j,prob[t][i][j]
    next_dir = choose_dir(next[max_i[t]][max_j[t]])
    # next_dir = dir_bunpu[t].index(max(dir_bunpu[t]))
    # next_dir2 = dir[randint(0,3)]
    ans += dir[next_dir]*move
    for _ in range(move):
        for ai in range(I):
            for aj in range(J):
                bi,bj = ai+di[next_dir],aj+dj[next_dir]
                if (ai,aj) == (ti,tj) or is_blocked(next_dir,ai,aj,bi,bj):
                    prob[t+1][ai][aj] += prob[t][ai][aj]
                else:
                    prob[t+1][ai][aj] += prob[t][ai][aj]*p
                    prob[t+1][bi][bj] += prob[t][ai][aj]*(1-p)
print(ans)