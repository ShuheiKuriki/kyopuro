# Part1：入力を受け取る
N = int(input()) #トーナメントの深さ
A = list(map(int, input().split())) #各人の結果を並べた配列
M = pow(2,N) #参加人数

# Part2：勝利数ごとに人の番号を記録
# best_to_win：「ベストa」を「勝利数」に変換する辞書（javaやC++でいうmap）
best_to_win = {pow(2,i):N-i for i in range(N+1)}
# people_nums[w]はw勝した人の番号を記録する配列
people_nums = [[] for w in range(N+1)]
for i,a in enumerate(A):
    num = i+1 #人の番号
    w = best_to_win[a] #num番の人の勝利数
    people_nums[w].append(num)

# Part3：トーナメント上に実際に人を配置
ans = [0]*M
for w in range(N+1):
    # w勝した人のトーナメント上の位置(1-index)を表す配列
    positions = [pos for pos in range(pow(2,w),M+1,pow(2,w+1))]
    # w勝した人の人数が位置の数と合わなければ-1を出力して終了
    if len(people_nums[w]) != len(positions):
        print(-1)
        exit()
    # トーナメント上の位置（pos）にnum番の人を配置
    for pos, num in zip(positions, people_nums[w]):
        ans[pos-1] = num
print(*ans)