class Dinic:
    """
        最大フロー問題
        https://atcoder.github.io/ac-library/production/document_ja/maxflow.html
        dinic法の非再帰実装
        verify:https://judge.u-aizu.ac.jp/onlinejudge/description.jsp?id=GRL_6_A
        計算量O(EV^2) or O(min(n^(2/3)m,m^(3/2)))（辺の容量が全て1）
    """
    _INF = 10**18

    def __init__(self, n=0):
        """
            _edges[i]:i番目に追加した有向辺の情報
                [始点の頂点番号, 始点が同じ辺のうち何番目に追加されたか]
            _edge[i][j]:頂点iを始点とするj番目の辺の情報
                [終点, 逆辺のid, 残り容量]
        """
        self._n = n
        self._edges = []
        self._edge = [[] for _ in range(n)]  # [to, rev, cap]

    def add_edge(self, from_, to, cap):
        """
            ・グラフに始点from_,終点to,容量capの辺を追加
            ・容量0の逆辺も追加
            return 何番目に追加した辺か
        """
        assert 0 <= from_ < self._n
        assert 0 <= to < self._n
        assert 0 <= cap
        m = len(self._edges)
        self._edges.append([from_, len(self._edge[from_])])
        from_id = len(self._edge[from_])
        to_id = len(self._edge[to])
        if from_ == to:
            to_id += 1
        self._edge[from_].append([to, to_id, cap])
        self._edge[to].append([from_, from_id, 0])
        return m

    def get_edge(self, i):
        """
            ・i番目に追加した辺の情報を返却
            return [始点, 終点, 辺の容量, 現在の流量]
        """
        assert 0 <= i < len(self._edges)
        _e = self._edge[self._edges[i][0]][self._edges[i][1]]
        _re = self._edge[_e[0]][_e[1]]
        return [self._edges[i][0], _e[0], _e[2] + _re[2], _re[2]]

    def get_all_edges(self):
        """
            ・全ての辺の情報を返却
            return [from_, to, cap, flow]のリスト
        """
        return [self.get_edge(i) for i in range(len(self._edges))]

    def change_edge(self, i, new_cap, new_flow):
        """
            ・i番目の辺について、(容量,流量)を(new_cap,new_flow)に変更
            ・逆辺以外の辺はそのまま
        """
        assert 0 <= i < len(self._edges)
        assert 0 <= new_flow <= new_cap
        _e = self._edge[self._edges[i][0]][self._edges[i][1]]
        _re = self._edge[_e[0]][_e[1]]
        _e[2] = new_cap - new_flow
        _re[2] = new_flow

    def _flow_bfs(self, s, t):
        """
            関数flow内部で実施するbfs
            sを根としてtにたどり着くまでbfsを行う
            return level
                level[i]: sを根とした際の頂点iの深さ
                tよりも前に到達できなかった頂点の深さは初期値-1のまま
        """
        level = [-1] * self._n
        level[s] = 0
        que = [s]
        while(que):
            next_que = []
            for v in que:
                for to, rev, cap in self._edge[v]:
                    if(cap == 0) or (level[to] >= 0):
                        continue
                    level[to] = level[v] + 1
                    if(to == t):
                        return level
                    next_que.append(to)
            que, next_que = next_que, que
        return level

    def flow(self, s, t, flow_limit=_INF):
        """
            現在の状況から新たに追加する形で、
            頂点sから頂点tまでflow_limitを超えない様にフローを流せるか試行する。
            （各辺の流量を更新する。）
            それ以上流せなくなるか、flow_limitに達した時点で終了する
            return 新たに流すことのできた流量
        """
        assert 0 <= s < self._n
        assert 0 <= t < self._n
        assert s != t

        flow = 0
        while(flow < flow_limit):
            level = self._flow_bfs(s, t)
            if(level[t] == -1):
                break

            iterator = [0] * self._n
            in_ = [0] * self._n
            out = [0] * self._n

            in_[t] = flow_limit - flow
            route = [t]
            while(route):
                v = route[-1]
                if(in_[v] == out[v]) and (v == t):
                    flow += out[t]
                    return flow
                if(v == s) or (in_[v] == out[v]):
                    route.pop()
                    w = route[-1]
                    flow_vw = in_[v]
                    i = iterator[w]
                    to, rev, cap = self._edge[w][i]
                    self._edge[v][rev][2] -= flow_vw
                    self._edge[w][i][2] += flow_vw
                    out[w] += flow_vw
                    continue

                for i in range(iterator[v], len(self._edge[v])):
                    to, rev, cap = self._edge[v][i]
                    if((level[to] == -1)
                       or (level[v] <= level[to])
                       or (self._edge[to][rev][2] == 0)):
                        continue
                    in_[to] = min(in_[v]-out[v], self._edge[to][rev][2])
                    out[to] = 0
                    route.append(to)
                    iterator[v] = i
                    break
                else:
                    iterator[v] = len(self._edge[v])
                    route.pop()
                    if(v == t):
                        if(out[t] == 0):
                            return flow
                        flow += out[t]
                        continue
                    w = route[-1]
                    flow_vw = out[v]
                    i = iterator[w]
                    to, rev, cap = self._edge[w][i]
                    self._edge[v][rev][2] -= flow_vw
                    self._edge[w][i][2] += flow_vw
                    out[w] += flow_vw
                    iterator[w] += 1
        return flow

    def min_cut(self, s):
        visited = [False] * self._n
        visited[s] = True
        que = [s]
        while(que):
            next_que = []
            for p in que:
                for to, rev, cap in self._edge[p]:
                    if(cap > 0) and (not visited[to]):
                        visited[to] = True
                        next_que.append(to)
            que, next_que = next_que, que
        return visited

import sys
input = sys.stdin.readline

N, M = map(int, input().split())
dinic = Dinic(N)
for i in range(M):
    u, v, c = map(int, input().split())
    dinic.add_edge(u, v, c)
ans = dinic.flow(0, N-1)
print(ans)