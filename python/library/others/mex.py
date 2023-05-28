def mex(lis):
    # setまたはlistの状態で受け取る
    now = 0
    for l in sorted(lis):
        if now==l:
            now += 1
        else:
            return now
    return now