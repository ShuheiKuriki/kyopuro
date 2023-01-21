# verify：https://atcoder.jp/contests/abc286/tasks/abc286_f
# 中国剰余定理
def crt(rs,mods):
    # all(x%m == r for m,r in zip(mods,rs))を満たすxを返す
    def extgcd(a, b): # ax+by=d
        if b==0:return a,1,0 # a*1+b*0=a(b=0のとき)
        d,y,x = extgcd(b,a%b)
        return d,x,y-(a//b)*x
    cum = 1
    r0 = rs[0]
    for r1,m in zip(rs,mods):
        if r0!=r1:
            _,x,_ = extgcd(cum,m)
            r0 = (cum*x*(r1-r0)+r0)%(cum*m)
        cum *= m
    return r0
