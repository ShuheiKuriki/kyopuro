#include <bits/stdc++.h>
using namespace std;
// #include <atcoder/all>
// using namespace atcoder;
// using mint = modint1000000007;
// using mint = modint998244353;
#define rep(i, n) for (int i = 0; i < (int)(n); i++)
#define rep2(i, a, b) for (int i = a; i < (int)(b); i++)
#define all(v) v.begin(), v.end()
using ll = long long;
const ll INF = 1e18;
// 変数定義
int N, M, a, b, ans;
vector<vector<int>> G;
vector<bool> visited;

void dfs(int v)
{
  for (auto next_v : G[v])
  {
    if (visited[next_v])
      continue;
    visited[next_v] = true;
    dfs(next_v);
  }
}
int main()
{
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  cin >> N >> M;
  G.assign(N, vector<int>(0));
  visited.assign(N, false);
  rep(i, M)
  {
    cin >> a >> b;
    a -= 1;
    b -= 1;
    G[a].push_back(b);
    G[b].push_back(a);
  }
  visited[0] = true;
  dfs(0);
  return 0;
}