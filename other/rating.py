from math import log2,exp,sqrt

def g(x):
  return pow(2.0,x/800)

def g_inv(y):
  return log2(y)*800

def f(x):
  return 1200*(sqrt((1+pow(0.9,x))/(1-pow(0.9,x)))-1)/(sqrt(19)-1)

def ave(N,A):
  total = 0
  for i,a in enumerate(A):
    total += g(a)* pow(0.9,i)
  return g_inv(total/(10*(1-pow(0.9,N))))

def h(x,y):
  t = x-y
  if t > 400:
    return t
  if x > 400:
    return 400 / exp( (400 - t) / 400 )
  return x/exp( y / 400 )


def predict(N,A):
  aver = ave(N,A)
  # print(aver)
  ans = round(h(aver,f(N)))
  return ans

def target(N,M,A):
  mini = 0
  maxi = 5000
  while mini+1<maxi:
    mid = (mini+maxi)//2
    p = predict(N+1,[mid]+A)
    if p == M:
      break
    if p<M: #予測が目標に届かないなら
      mini = mid
    else:
      maxi = mid
  return mid

s = input()
A = list(map(int, input().split()))
N = len(A)
if s == 'pred' or s == 'predict':
  print(predict(N,A))
else:
  M = int(s)
  print(target(N,M,A))


# for i in range(1,21):
#   print(f(i))

#上がりすぎた時、下がりすぎた時にペナルティが存在する

# 1200.0
# 745.413209167406
# 545.1360660734734
# 426.7318318944591
# 346.81280099957945
# 288.62076131583717
# 244.12623521104516
# 208.93228764736358
# 180.39932641532826
# 156.83200284236486
# 137.0834071590981
# 120.34498520255892
# 106.02725556583351
# 93.68831386604991
# 82.98902775369449
# 73.66388965251993
# 65.50144170744184
# 58.330762175570875
# 52.01190858270876
# 46.4290132644494

# marroncastle917
# 2210 2142 1394 1660 1608 1984 2400 1426 1807 1882 1914 1920 1743 2286 1436 1309 2361 916 1290 1621 1441 1597 1492 1578 1818 1059 153 1767 1251 1098 1755 1402 765 1790 1261 1399 1295 1608 1395 1978 1668 1228 1731 1337 893 188 1250 1166 973 705 547 704 
#zombie8
# 386 481 266 118 192 392 680 845 622 294 560 233 350 266 572 272 815 555 365 140 1113 49