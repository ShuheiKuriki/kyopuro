import sys; input = sys.stdin.readline
I = lambda:map(int,input().split())
comp = lambda arr: {e: i for i, e in enumerate(sorted(set(arr)))}
comp2 = lambda arr: {i: e for i, e in enumerate(sorted(set(arr)))}
A = [tuple(I()) for _ in range(int(*I()))]
X = [a[0]for a in A]+[a[0]+a[3]for a in A]
Y = [a[1]for a in A]+[a[1]+a[4]for a in A]
Z = [a[2]for a in A]+[a[2]+a[5]for a in A]
compX,compX2,compY,compY2,compZ,compZ2 = comp(X),comp2(X),comp(Y),comp2(Y),comp(Z),comp2(Z)
lx,ly,lz = len(compX),len(compY),len(compZ)
imos = [[[0]*(lz+1)for _ in range(ly+1)]for _ in range(lx+1)]
for x,y,z,w,h,v in A:
    xw,yh,zv = compX[x+w],compY[y+h],compZ[z+v]
    x,y,z = compX[x],compY[y],compZ[z]
    imos[x][y][z] += 1
    imos[xw][y][z] -= 1
    imos[x][yh][z] -= 1
    imos[x][y][zv] -= 1
    imos[x][yh][zv] += 1
    imos[xw][y][zv] += 1
    imos[xw][yh][z] += 1
    imos[xw][yh][zv] -= 1
for x in range(lx):
    for y in range(ly+1):
        for z in range(lz+1):imos[x+1][y][z] += imos[x][y][z]
for x in range(lx+1):
    for y in range(ly):
        for z in range(lz+1):imos[x][y+1][z] += imos[x][y][z]
for x in range(lx+1):
    for y in range(ly+1):
        for z in range(lz):imos[x][y][z+1] += imos[x][y][z]
print(sum((compX2[x+1]-compX2[x])*(compY2[y+1]-compY2[y])*(compZ2[z+1]-compZ2[z])for x in range(lx-1)for y in range(ly-1)for z in range(lz-1)if imos[x][y][z]))