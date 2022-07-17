import sys
input = sys.stdin.readline
write = sys.stdout.write
flush = sys.stdout.flush

def query(x):
    write(str(x)+"\n")
    flush()

class UnionFind():
    def __init__(self, n):
        self.n = n
        self.parents = [-1] * n

    def find(self, x):
        if self.parents[x] < 0:
            return x
        else:
            self.parents[x] = self.find(self.parents[x])
        return self.parents[x]

    def union(self, x, y):
        x = self.find(x)
        y = self.find(y)

        if x == y:
            return

        if self.parents[x] > self.parents[y]:
            x, y = y, x

        self.parents[x] += self.parents[y]
        self.parents[y] = x

    def same(self, x, y):
        return self.find(x) == self.find(y)

    def roots(self):
        return [i for i, x in enumerate(self.parents) if x < 0]

    def members(self, x):
        root = self.find(x)
        return [i for i in range(self.n) if self.find(i) == root]

    def size(self,x):
        return abs(self.parents[self.find(x)])

    def groups(self):
        roots = self.roots()
        r_to_g = {}
        for i, r in enumerate(roots):
            r_to_g[r] = i
        groups = [[] for _ in roots]
        for i in range(self.n):
            groups[r_to_g[self.find(i)]].append(i)
        return groups

N = 400
M = 1995
def build(edges, preds, adopt):
    adopt = [-1 if a>=10 else a for a in adopt]
    not_decided = []
    uf = UnionFind(N)
    # cnt = 0
    for i,(u,v) in enumerate(edges):
        if adopt[i]==1:
            uf.union(u,v)
            # cnt += 1
        elif adopt[i]==-1:
            not_decided.append((preds[i], i))
    not_decided.sort()
    # max_adopt = 0
    for p,i in not_decided:
        u,v = edges[i]
        if adopt[i] == -1:
            if uf.same(u,v):
                adopt[i] = 10
            else:
                adopt[i] = 11
                uf.union(u,v)
                # cnt += 1
                # if cnt == N-1:
                    # max_adopt = p
    # return max_adopt, adopt
    return adopt

def solve(X,Y,edges,const,L):
    preds = [((X[v]-X[u])**2+(Y[v]-Y[u])**2)*const for u,v in edges]
    dists = 0
    adopt = build(edges, preds, [-1]*M)
    # max_adopt, adopt = build(edges, preds, [-1]*M)
    for i in range(M):
        l = L[i]
        p = preds[i]
        preds[i] = l*l
        if not ((adopt[i] == 11 and l*l <= p) or (adopt[i] == 10 and l*l > p)):
            adopt = build(edges, preds, adopt)
            # max_adopt, adopt = build(edges, preds, adopt)
        adopt[i] -= 10
        if adopt[i]==1:
            dists += l
        # query(adopt[i])
    return dists

if __name__=="__main__":
    X,Y = [0]*N,[0]*N
    for i in range(N): X[i],Y[i] = map(int, input().split())
    edges = [tuple(map(int, input().split())) for _ in range(M)]
    L = [int(input()) for _ in range(M)]
    for const in range(25,36):
        print(const/10, solve(X,Y,edges,const/10,L))
    # solve(X,Y,edges)