import sys; input = sys.stdin.readline
I = lambda: map(int,input().split())

from collections import*
from enum import Enum
from typing import List
INF = 10**18

class UnionFind():
    def __init__(self, n):
        self.n = n
        self.parents = [-1] * n

    def find(self, x):
        if self.parents[x] < 0: return x
        # 経路圧縮
        self.parents[x] = self.find(self.parents[x])
        return self.parents[x]

    def union(self, x, y):
        x = self.find(x); y = self.find(y)
        if x == y: return
        # マージテク
        if self.parents[x] > self.parents[y]: x,y = y,x
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

class Pos:
    def __init__(self, y: int, x: int):
        self.y = y
        self.x = x

    def calc_dist(self, pos):
        return abs(self.x - pos.x) + abs(self.y - pos.y)


class Response(Enum):
    NOT_BROKEN = 0
    BROKEN = 1
    FINISH = 2
    INVALID = -1


class Field:

    def __init__(self, N: int, C: int):
        self.C = C
        self.is_broken = [[False]*N for _ in range(N)]
        self.hardness = [[0]*N for _ in range(N)]
        self.total_cost = 0

    def query(self, y: int, x: int, power: int) -> Response:
        self.total_cost += power + self.C
        print(f"{y} {x} {power}", flush=True)
        res = Response(int(input()))
        if res in (Response.BROKEN, Response.FINISH):
            self.is_broken[y][x] = True
        # print(f"power: {power}",file=sys.stderr)
        self.hardness[y][x] += power
        return res


class Solver:

    def __init__(self, N: int, source_pos: List[Pos], house_pos: List[Pos], W: int, K: int, C: int):
        self.N = N
        self.source_pos = source_pos
        self.house_pos = house_pos
        self.nearest_source = [source_pos[0] for _ in house_pos]
        self.moves = []
        self.W = W
        self.K = K
        self.C = C
        self.field = Field(N, C)
        self.power_memory = deque([])

    def solve(self):
        self.mst()
        # from each house, go straight to the first source
        for pos1, pos2 in self.moves:
            self.move(pos1, pos2)

        # should receive Response.FINISH and exit before entering here
        raise AssertionError()

    def mst(self):
        edges = defaultdict(lambda:[])
        cnt = 0
        for k1,pos1 in enumerate(self.house_pos):
            for k2,pos2 in enumerate(self.house_pos[:k1]):
                dist = pos1.calc_dist(pos2)
                edges[dist].append(((k1,pos1),(k2,pos2)))
            for w2,pos2 in enumerate(self.source_pos):
                dist = pos1.calc_dist(pos2)
                edges[dist].append(((k1,pos1),(self.K+w2,pos2)))
                cnt += 1
        for w1,pos1 in enumerate(self.source_pos):
            for w2,pos2 in enumerate(self.source_pos[:w1]):
                edges[0].append(((self.K+w1,pos1),(self.K+w2,pos2)))

        dists = sorted(edges.keys())
        vnum = self.W + self.K
        uf = UnionFind(vnum)
        for d in dists:
            for (v1,pos1),(v2,pos2) in edges[d]:
                if uf.same(v1,v2):continue
                uf.union(v1,v2)
                if d > 0:
                    self.moves.append((pos1,pos2))

    def get_next_power(self, power: int):
        # print(power,file=sys.stderr)
        # self.power_memory.append(power)
        # if len(self.power_memory)>5:
        #     self.power_memory.popleft()
        # return max(1, sum(self.power_memory)//len(self.power_memory)//3)
        return max(1, power//3)
        # return 100

    def move(self, start: Pos, goal: Pos):
        # you can output comment
        print(f"# move from ({start.y},{start.x}) to ({goal.y},{goal.x})",file=sys.stderr)
        power = 100
        # self.power_memory.append(power)

        # down/up
        # print(power,file=sys.stderr)
        if start.y < goal.y:
            for y in range(start.y, goal.y, 1):
                power = self.get_next_power(self.destruct(y, start.x, power)) 
        else:
            for y in range(start.y, goal.y, -1):
                power = self.get_next_power(self.destruct(y, start.x, power))  

        # right/left
        if start.x < goal.x:
            for x in range(start.x, goal.x + 1, 1):
                power = self.get_next_power(self.destruct(goal.y, x, power))   
        else:
            for x in range(start.x, goal.x - 1, -1):
                power = self.get_next_power(self.destruct(goal.y, x, power))   

        # self.destruct(start.y, start.x, power)
        # now = Pos(start.y, start.x)
        # dir_x = [-1,1][goal.x>start.x]# if goal.x != start.x else 0
        # dir_y = [-1,1][goal.y>start.y]# if goal.y != start.y else 0
        # while now.x != goal.x or now.y != goal.y:
        #     step = max(1, min([abs(now.x-goal.x), abs(now.y-goal.y), 3]))
            
        #     # down/up
        #     hard_x = hard_y = INF
        #     if now.x != goal.x:
        #         s_x, e_x = sorted((now.x+dir_x, now.x+dir_x*step))
        #         hard_x = sum(self.destruct(now.y, x, power)for x in range(s_x, e_x+1))
        #     if now.y != goal.y:
        #         s_y, e_y = sorted((now.y+dir_y, now.y+dir_y*step))
        #         hard_y = sum(self.destruct(y, now.x, power)for y in range(s_y, e_y+1))
        #     # print("#",hard_x,hard_y,s_y,e_y)
        #     if hard_x < hard_y:
        #         now.x = e_x
        #     else:
        #         now.y = e_y
        #     power = self.get_next_power(min(hard_x, hard_y)//step)
        #     # print(now.y,now.x,file=sys.stderr)

    def destruct(self, y: int, x: int, power: int):
        # excavate (y, x) with given power
        while not self.field.is_broken[y][x]:
            result = self.field.query(y, x, power)
            if result == Response.FINISH:
                # print(f"total_cost={self.field.total_cost}", file=sys.stderr)
                sys.exit(0)
            elif result == Response.INVALID:
                print(f"invalid: y={y} x={x}", file=sys.stderr)
                sys.exit(1)
        # print(self.field.hardness[y][x],file=sys.stderr)
        return self.field.hardness[y][x]


def main():
    N, W, K, C = I()
    print(f"W: {W}, K: {K}, C: {C}\t", end="", file=sys.stderr)
    source_pos = [Pos(*I())for _ in range(W)]
    house_pos = [Pos(*I())for _ in range(K)]

    solver = Solver(N, source_pos, house_pos, W, K, C)
    solver.solve()


if __name__ == "__main__":
    main()
