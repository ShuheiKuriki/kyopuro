dxy = [(-1,0), (1,0), (0,-1), (0,1)]
make_dir = 'udlr' #人が仕切りを作る
move_dir = 'UDLR' #人やペットが移動する
make_dic = {'u':0,'d':1,'l':2,'r':3}
move_dic = {'U':0,'D':1,'L':2,'R':3}
H = W = 30

# マスがオフィス内か判定
def is_inner(x, y):
    return 1 <= x <= H and 1 <= y <= W

# マスに物があるか
def exist(x,y):
    if room[x][y]==-1: return False
    return sum(room[x][y]) > 0

# マスにペットがいるか
def pet_exist(x,y):
    if room[x][y]==-1: return False
    return sum(room[x][y][1:]) > 0

# マス(x,y)に仕切りを置けるかどうか判定
def check_cell(x, y):
    if not is_inner(x,y): return False
    # その場所に既に何かあれば不可
    if exist(x,y): return False
    # 隣のセルの配列pxy
    pxy = [(x+dx,y+dy) for dx,dy in dxy if is_inner(x+dx,y+dy)]
    # 隣にペットがいれば不可
    return not any(pet_exist(px,py) for px,py in pxy)

# 人hがmd方向に仕切りを作る
def make_partition(hx,hy,md):
    dx, dy = dxy[make_dic[md]]
    bx, by = hx + dx, hy + dy;
    if check_cell(bx,by): room[bx][by] = -1
    return room[bx][by] == -1

# ペットpをmd方向に動かす
def move_pet(p,md):
    if md not in move_dir: return
    dx, dy = dxy[move_dic[md]]
    px, py, pt = pet[p]
    room[px][py][pt] -= 1
    px += dx; py += dy
    pet[p] = [px, py, pt]
    room[px][py][pt] += 1

# 人hをmd方向に動かす
def move_human(hx,hy,md):
    if md not in move_dir: return False
    dx, dy = dxy[move_dic[md]]
    room[hx][hy][0] -= 1;
    hx += dx; hy += dy;
    human[h] = [hx, hy]
    room[hx][hy][0] += 1;
    return True

# -1：通行不可（仕切りがある）
# [0]：人の人数
# [1~5]：ペットの数
room = [[[0]*6 for _ in range(W+1)] for _ in range(H+1)]
import sys
args = sys.argv
area = int(args[1])
# area = 15

# ペット情報を入力
N = int(input())
pet = [list(map(int, input().split())) for _ in range(N)]
for x,y,t in pet: room[x][y][t] += 1

# 人情報を入力
M = int(input())
human = [list(map(int, input().split())) for _ in range(M)]
for x,y in human: room[x][y][0] += 1

# 人のルートを決定
routes = [""]*M
for h,(x,y) in enumerate(human):
    if area < 30:
        routes[h] += "L"*(y-1)
        routes[h] += "U"*(x-area) if x>=area else "D"*(area-x)
        if h==0:
            routes[h] += "."*(60-len(routes[h]))
            routes[h] += ("dR"*area)[:-1] + ("rU"*area)[:-1]
    routes[h] += "."*(300-len(routes[h]))
    routes[h] = routes[h][::-1]

for _ in range(300):
    ope = ""
    for h,(hx, hy) in enumerate(human):
        op = routes[h][-1]
        if op == ".":
            done = True
        elif op in move_dir:
            done = move_human(hx, hy, op)
        else:
            done = make_partition(hx, hy, op)
        if done:
            ope += op
            routes[h] = routes[h][:-1]
        else:
            ope += '.';
    print(ope)

    for p,pm in enumerate(input().split()):
        for m in pm: move_pet(p, m)
