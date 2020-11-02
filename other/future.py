import sys
from copy import copy

def c_time(X):
    # X = [床の数, 壁の数]
    t = X[0] + X[1]*(X[1]+1)/2
    return int(t)

def main():
    # このコードは標準入力と標準出力を用いたサンプルコードです。
    # このコードは好きなように編集・削除してもらって構いません。
    # ---
    # This is a sample code to use stdin and stdout.
    # Edit and remove this code as you like.

    n,m = [5, 5]
    maze = [0]*n
    inputs = [["#","S","#","#","."],
              ["#","#","#","#","#"],
              [".","#","#","#","#"],
              [".","#","#","#","#"],
              [".",".",".",".","G"]]
    for i in range(n):
      s = inputs[i]
      maze[i] = [0]*m
      for j in range(m):
        if s[j] == "S":
          S = [i,j]
        if s[j] == "G":
          G = [i,j]
        maze[i][j] = s[j]
    # print("S:",S)
    mins = [0]*n
    for i in range(n):
      mins[i] = [[1000,1000]]*m
    mins[S[0]][S[1]] = [0,0]
    # print(mins)
    update = 1
    while update>0:
      update = 0
      for i in range(n):
        for j in range(m):
          if [i,j] != S:
            comp = []
            if i != 0:
              comp.append(copy(mins[i-1][j]))
            if i != n-1:
              comp.append(copy(mins[i+1][j]))
            if j != 0:
              comp.append(copy(mins[i][j-1]))
            if j != m-1:
              comp.append(copy(mins[i][j+1]))
            # print(comp)
            for k in range(len(comp)):
              if maze[i][j] == '.' or maze[i][j] == 'G':
                comp[k][0] += 1
              if maze[i][j] == '#':
                comp[k][1] += 1
            # print(comp)
            mini = mins[i][j]
            print("mini:",c_time(mini))
            for k in range(len(comp)):
              # print(c_time(comp[k]))
              if c_time(comp[k]) < c_time(mini):
                mini = comp[k]
            print("mini:",c_time(mini))
            if c_time(mini) < c_time(mins[i][j]):
              mins[i][j] = mini
              update += 1
            print("update:",update)
          print(mins)

    print(c_time(mins[G[0]][G[1]]))






if __name__ == '__main__':
    main()