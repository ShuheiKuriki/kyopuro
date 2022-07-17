from math import log
def f(y):
    return (pow(2,-10*y)-pow(2,-20*y))/(10*log(2))

for i in range(1,31):
    print(i,f((i/30)**2)*1e10)