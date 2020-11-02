def SA_IS(s, with_lcp = False):
  a = s + [0]
  # a = [aa+1 for aa in a] + [0] # <- 元の列にZeroが含まれるときはこっち
  k = max(a) + 1
  n = len(a)
  
  def induce_l(sa, a, n, k, stype):
    bucket = get_buckets(a, k, 1)
    for i in range(n):
      j = sa[i] - 1
      if j >= 0 and (not stype[j]):
        sa[bucket[a[j]]] = j
        bucket[a[j]] += 1
  
  def induce_s(sa, a, n, k, stype):
    bucket = get_buckets(a, k, 0)
    for i in range(n)[::-1]:
      j = sa[i] - 1
      if j >= 0 and stype[j]:
        bucket[a[j]] -= 1
        sa[bucket[a[j]]] = j
  
  def get_buckets(a, k, start = 0):
    bucket = [0] * k
    for item in a:
      bucket[item] += 1
    s = 0
    for i in range(k):
      s += bucket[i]
      bucket[i] = s - (bucket[i] if start else 0)
    return bucket
  
  def set_lms(a, n, k, default_order):
    bucket = get_buckets(a, k)
    sa = [-1] * n
    for i in default_order[::-1]:
      bucket[a[i]] -= 1
      sa[bucket[a[i]]] = i
    return sa
  
  def induce(a, n, k, stype, default_order):
    sa = set_lms(a, n, k, default_order)
    induce_l(sa, a, n, k, stype)
    induce_s(sa, a, n, k, stype)
    return sa
  
  def rename_LMS_substring(sa, a, n, stype, LMS, l):
    sa = [_s for _s in sa if LMS[_s]]
    tmp = [-1] * (n//2) + [0]
    dupl = 0
    for _ in range(1, l):
      i, j = sa[_-1], sa[_]
      for ii in range(n):
        if a[i+ii] != a[j+ii] or stype[i+ii] != stype[j+ii]:
          break
        if ii and (LMS[i+ii] or LMS[j+ii]):
          dupl += 1
          break
      tmp[j//2] = _ - dupl
    tmp = [t for t in tmp if t >= 0]
    return tmp, dupl
  
  def calc(a, n, k):
    stype = [1] * n
    for i in range(n-1)[::-1]:
      if a[i] > a[i+1] or (a[i] == a[i+1] and stype[i+1] == 0):
        stype[i] = 0
    
    LMS = [1 if stype[i] and not stype[i-1] else 0 for i in range(n-1)] + [1]
    l = sum(LMS)
    lms = [i for i in range(n) if LMS[i]]
    sa = induce(a, n, k, stype, lms)
    renamed_LMS, dupl = rename_LMS_substring(sa, a, n, stype, LMS, l)
    
    if dupl:
      sub_sa = calc(renamed_LMS, l, l - dupl)
    else:
      sub_sa = [0] * l
      for i in range(l):
        sub_sa[renamed_LMS[i]] = i
    
    lms = [lms[sub_sa[i]] for i in range(l)]
    sa = induce(a, n, k, stype, lms)
    return sa
  
  sa = calc(a, n, k)
  sa = sa[1:]
  n -= 1
  if not with_lcp:
    return sa
  
  rank = [0] * n
  for i in range(n):
    rank[sa[i]] = i
  lcp = [0] * (n - 1)
  h = 0
  for i in range(n):
    if h: h -= 1
    if rank[i] == 0: continue
    j = sa[rank[i] - 1]
    while j + h < n and i + h < n:
      if s[j+h] != s[i+h]: break
      h += 1
    lcp[rank[i] - 1] = h
  return sa, lcp

S = [ord(a)-96 for a in input()]
N = len(S)
sa, lcp = SA_IS(S, True)
print(sa,lcp)
