import numpy as np

# トエイボナッチ数列
first= [1,0,5]
for i in range(25):
    next= first[i]+first[i+1]+first[i+2]
    first.append(next)
print(first[-1])

# 約数の和
num = 1234567890
root = int(np.sqrt(num))
# print(root)
yakusuu = []
for i in range(root):
    if num%(i+1) == 0:
        j = num/(i+1)
        yakusuu.append(int(i+1))
        yakusuu.append(int(j))
        # print(i+1,j)
yakusuu= np.array(yakusuu)
yaku = yakusuu[yakusuu<10000001]

print(np.sum(yaku))


# 世界のナベアツ
sum=0
for i in range(20000):
    if i%3==0 or i%10 ==3 or (i//10)%10==3 or (i//100)%10==3 or (i//1000)%10==3:
        sum+=i
        # print(i)
print(sum)

# 全ての桁の積を求め続ける
num = 1000000
prod_list = []
for i in range(num):
    n_list = list(str(i))
    prod = 1
    for j in n_list:
        j = int(j)
        prod *= j
    prod_list.append(prod)
counts = 0
for i in range(num):
    # print(i)
    count = 0
    next = i
    while len(list(str(next)))>1:
        next = prod_list[next]
        # print(next)
        count +=1
    # print(count)
    if count == 7:
        counts += 1
print("answer:",counts)

# ローマ数字表記で8桁になる数の和
sum = 0
NUM = 1001
length = [0,1,2,3,2,1,2,3,4,2]
for num in range(1001):
#     NM = num//1000
# # ND = (num%1000)//500
#     NC = (num%1000)//100
# # NL = (num%100)//50
#     NX = (num%100)//10
# # NV = (num%10)//5
#     NI = (num%10)
# print(NM,NC,NX,NI)
    digit = 0
    n_list = list(str(num))
    for j in n_list:
        j = int(j)
        digit += length[j]
    if digit == 8:
        sum += num
print(sum)

# 667回目の13日の金曜日
month_list = [31,28, 31,30,31,30,31,31,30,31,30,31]
month_list2 = [31,29, 31,30,31,30,31,31,30,31,30,31]
days =0
count = 0
year = 2009
while count<667:
    year+=1
    month = 0
    if year % 4 == 0:
        months = month_list2
    else:
        months = month_list
    while count<667 and month <12:
        month += 1
        if (days+13)%7 == 2:
            count += 1
        days += months[month-1]
        # print(month,count,days)
    # print(year)
print(year, month, 13)
