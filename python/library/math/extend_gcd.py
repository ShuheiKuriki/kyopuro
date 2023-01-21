# 拡張ユークリッド互除法
def extgcd(a, b): # ax+by=dを満たすd,x,yを返す
    if b==0: return a,1,0 # a*1+b*0=a(b=0の場合)
    d,y,x = extgcd(b,a%b)
    return d,x,y-(a//b)*x