import sys; input = sys.stdin.readline
I = lambda:map(int,input().split())
W,H,T = I();sx,sy = I();tx,ty = I()
def calc(i):
    a = (i+1)*W-tx-sx if i%2 else tx+i*W-sx
    if abs(a)>T:return 0
    bb = int((T*T-a*a)**.5)
    lis = set([-(bb+1),-bb,-(bb-1),bb-1,bb,bb+1])
    res = set()
    for b in lis:
        # b = (j+1)*H-ty-sy if j%2 else ty+j*W-sy
        if a*a+b*b==T*T:
            if (b+ty+sy)%H==0 and ((b+ty+sy)//H-1)%2:
                res.add(b)
            elif (b-ty+sy)%H==0 and (b-ty+sy)//H%2==0:
                res.add(b)
    return len(res)
print(sum(calc(i)for i in range(-T-10,T+11)))