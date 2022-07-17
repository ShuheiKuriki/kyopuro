from random import *
from math import exp
from time import time

def calc_score():
    score = 0
    return score

def modify():
    return

def annealing():
    t_limit = 1.8
    s_temp, e_temp = 1000, 100
    max_step = 10000
    score = 0
    for step in range(max_step):
        temp = (s_temp*(max_step-step)+e_temp*step)//max_step
        modify()
        new_score = calc_score()
        if new_score > score or exp((new_score-score)/temp) > random():
            # 遷移を採用する
            score = new_score
        n_time = time() - s_time
        if step % 1000 == 0: print(n_time, score)
        if n_time > t_limit: break
    return score

s_time = time()
score = annealing()
print(score)
ans = []
for a in ans: print(*a)