import sys; input = sys.stdin.readline
f = lambda:map(int,input().split())
# grundy数が0の状態で回ってきたプレイヤーが負け
def solve():
    grundy = 0
    return grundy==0
# Takahashi君が先手の場合、grundy数が0なら後手のAoki君が勝利する
print(['Takahashi','Aoki'][solve()])