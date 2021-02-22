// g++ A.cpp -std=c++14 -I . && ./a.out
#include <bits/stdc++.h>
using namespace std;
// #include <atcoder/all>
// using namespace atcoder;
// using mint = modint1000000007;
// using mint = modint998244353;
#define rep(i, n) for (int i = 0; i < (int)(n); i++)
#define rep2(i, a, b) for (int i = a; i < (int)(b); i++)
#define rrep(i, a, b) for (int i = a; i > (int)(b); i--)
#define all(v) v.begin(), v.end()
using ll = long long;
using P = pair<long long, long long>;
const ll INF = 1e18;
// 変数定義
ll N, M, u, v, d, r, total, cnt, ans;
struct edge {ll to, cost;};
vector<vector<edge>> G;
vector<ll> dist;

// P(距離, 頂点)
void dijkstra(int s) {
  priority_queue<P, vector<P>, greater<P>> que;
  dist.assign(N, INF);
  dist[s] = 0;
  que.push(P(0, s));
  while (!que.empty()) {
    P p = que.top(); que.pop();
    tie(d,v) = p;
    if (dist[v]!=d) continue;
    for (auto e: G[v]) {
      ll new_d = dist[v] + e.cost;
      if (new_d<dist[e.to]) {
        dist[e.to] = new_d;
        que.push(P(new_d, e.to));
      }
    }
  }
}
int main()
{
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  cin >> N >> M >> r;
  G.assign(N, vector<edge>());
  rep(i, M)
  {
    cin >> u >> v >> d;
    G[u].push_back(edge{v, d});
  }
  dijkstra(r);
  rep(i,N) {
    if (dist[i]==INF) cout << "INF" << '\n';
    else cout << dist[i] << '\n';
  }
  return 0;
}