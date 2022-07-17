dxy = [(1,0), (0,1), (-1,0), (0,-1)]
make_dir = 'drul' #人が仕切りを作る
move_dir = 'DRUL' #人やペットが移動する
make_dic = {'d':0,'r':1,'u':2,'l':3}
move_dic = {'D':0,'R':1,'U':2,'L':3}
H = W = 30

# マスがオフィス内か判定
def is_inner(x, y):
    return 1 <= x <= H and 1 <= y <= W

# マスに物があるか
def exist(x,y):
    if room[x][y]==-1: return False
    return sum(room[x][y]) > 0

# マスにいるペットの数
def pet_num(x,y):
    if room[x][y]==-1: return 0
    return sum(room[x][y][1:])

# マス(x,y)に仕切りを置けるかどうか判定
def check_cell(x, y):
    if not is_inner(x,y): return False
    # その場所に既に何かあれば不可
    if exist(x,y): return False
    # 隣のセルの配列pxy
    pxy = [(x+dx,y+dy) for dx,dy in dxy if is_inner(x+dx,y+dy)]
    # 隣にペットがいれば不可
    return not any(pet_num(px,py)>0 for px,py in pxy)

# 人hがmd方向に仕切りを作る
# 1：作成成功
# 0：作成済みのため何もしない
# -1：作成不可のため何もせず次に持ち越し
def make_partition(hx,hy,md):
    dx, dy = dxy[make_dic[md]]
    bx, by = hx + dx, hy + dy;
    if room[bx][by] == -1: return 0
    if check_cell(bx,by):
        room[bx][by] = -1
        return 1
    return -1

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
# 1：移動成功（opはそのままで次へ）
# 0：移動不可能(基本的にはないはず)
def move_human(hx,hy,md):
    # if md not in move_dir: return False
    dx, dy = dxy[move_dic[md]]
    nx, ny = hx+dx, hy+dy
    if not is_inner(nx, ny) or room[nx][ny]==-1: return 0
    room[hx][hy][0] -= 1;
    human[h] = [nx, ny]
    room[nx][ny][0] += 1;
    return 1

def get_area_pet_num(x1, x2, y1, y2):
    return sum(pet_num(x,y)for x in range(x1,x2+1)for y in range(y1,y2+1))

def get_pet_nums():
    lis = [(get_area_pet_num(1,27,i,i),i) for i in range(1,maxy+1) if closed[i]==0]
    if not closed[-1]: lis += [(get_area_pet_num(1,30,maxy+2,30),maxy+1)]
    if len(lis)==0: return [],[]
    lis.sort(reverse=True)
    pet_nums,inds = zip(*lis)
    return list(inds), list(pet_nums)

def get_route(sx,sy,gx,gy):
    ud = 'D'*(gx-sx) if sx < gx else 'U'*(sx-gx)
    lr = 'R'*(gy-sy) if sy < gy else 'L'*(sy-gy)
    return lr + ud
# -1：通行不可（仕切りがある）
# [0]：人の人数
# [1~5]：ペットの数
room = [[[0]*6 for _ in range(W+1)] for _ in range(H+1)]

# ペット情報を入力
N = int(input())
pet = [list(map(int, input().split())) for _ in range(N)]
dog = 0
for x,y,t in pet:
    room[x][y][t] += 1
    if t==4: dog += 1
# 人情報を入力
M = int(input())
human = [list(map(int, input().split())) for _ in range(M)]
for x,y in human: room[x][y][0] += 1

# phase3で移動する各象限の真ん中の位置

# phase1での目的地と経路を決定
goals = [(1,(3+h*4)%28)for h in range(M)]
routes = [""]*M
for h in range(M):
    routes[h] = get_route(*human[h],*goals[h])[::-1]
phase = 1
# status 1  ：成功、opeにopをそのまま追加しroutes[h]をpop
# status 0  ：済み、opeに'.'を追加しroutes[h]をpop
# status -1 ：持越、opeに'.'を追加しroutes[h]はそのまま
for i in range(300):
    print("#",i,phase)
    ope = ""
    empty_route = 0
    for h in range(M):
        if len(routes[h])==0:
            empty_route |= 1<<h
            op = "."
        else:
            op = routes[h][-1]
        if op == ".":
            status = 1
        elif op in move_dir:
            status = move_human(*human[h], op)
        else:
            status = make_partition(*human[h], op)
        # 実際にやる操作をopeに追加
        ope += op if status == 1 else '.'
        # 実施済みの操作をpop
        if status >= 0: routes[h] = routes[h][:-1]
    print(ope)

    for p,pm in enumerate(input().split()):
        for m in pm: move_pet(p, m)

    if phase == 1: #一番上に移動
        if empty_route == (1<<M)-1:
            for h in range(M):
                routes[h] = ('lrD'*29)[::-1]
            phase = 2

    elif phase == 2: #壁を作る
        if empty_route == (1<<M)-1:
            if i <= 150:
                for h in range(M):
                    if M==5 and h>=1 or M==6 and h>=4:
                        new_goal = (1, 4*(M+h//2%2)+3) if M==5 else (1, 27)
                        routes[h] = get_route(30,goals[h][1],*new_goal)[::-1]
                phase = 3
                maxy = 27
            else:
                phase = 5
                maxy = min(27,4*M-1)
                direction = [0]*M
                closed = [(h+1)%2 for h in range(maxy+1)] + [-1]
                if dog:
                    routes[0] = get_route(*human[0],1,30)[::-1]

    elif phase == 3: #一番上に移動2回目
        if empty_route == (1<<M)-1:
            for h in range(M):
                if M>6: continue
                if M==5 and h>=1 or M==6 and h>=4:
                    routes[h] = (('lr'[h%2]+'D')*29)[::-1]
            phase = 4

    elif phase == 4: #壁を作る
        if empty_route == (1<<M)-1:
            phase = 5
            direction = [0]*M
            closed = [(h+1)%2 for h in range(maxy+1)] + [-1]
            if dog:
                routes[0] = get_route(30,goals[0][1],1,30)[::-1]

    elif phase == 5: #エリアを閉じる
        inds, pet_nums = get_pet_nums()
        print("#",pet_nums[:10])
        print("#",maxy)
        if dog and human[0][1]==30 and closed[-1]==-1:
            closed[-1] = 0
            continue
        for h in range(M):
            if routes[h]=='':
                y = human[h][1]
                if y<=1: direction[h] = 1
                if y>=maxy: direction[h] = 0
                routes[h] += 'LR'[direction[h]]*2
                if y in inds and not closed[y]:
                    rank = inds.index(y)
                    if rank <= 5 and pet_nums[rank] >= 1:
                        routes[h] += 'u'
                        closed[y] = 1
                if y==maxy and closed[-1]==0:
                    if maxy+1 not in inds: continue
                    rank2 = inds.index(maxy+1)
                    close_index = 3 if dog else 2
                    if pet_nums[rank2] >= close_index:
                        routes[h] += 'r'
                        closed[-1] = 1
