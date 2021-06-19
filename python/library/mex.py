def mex(lis):
    # setの状態で受け取る
    lis = list(lis)
    lis.sort()
    now = 0
    for l in lis:
        if now==l:
            now += 1
        else:
            return now
    return now