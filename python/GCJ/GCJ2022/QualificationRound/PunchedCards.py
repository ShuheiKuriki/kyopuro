import sys,os,io
input = sys.stdin.readline
#input = io.BytesIO(os.read(0,os.fstat(0).st_size)).readline
T = int(input())
ans = []
for t in range(1,T+1):
    R, C = map(int, input().split())
    ans.append(f"Case #{t}:")
    ans.append(".."+"+-"*(C-1)+"+")
    for i in range(R):
        if i==0:
            ans.append("."+".|"*C)
        else:
            ans.append("|"+".|"*C)
        ans.append("+"+"-+"*C)
print(*ans, sep='\n')