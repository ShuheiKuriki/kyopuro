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
vector<int> dp;

int dfs(int v)
{
  if (visited[v])
    return dp[v];
  // cout << v << '\n';
  for (auto next_v : G[v])
  {
    dp[v] += dfs(next_v);
  }
  visited[v] = true;
  return dp[v];
}
int main()
{
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  cin >> N >> M;
  G.assign(N, vector<int>(0));
  visited.assign(N, false);
  dp.assign(N, 0);
  rep(i, M)
  {
    cin >> a >> b;
    a -= 1;
    b -= 1;
    G[a].push_back(b);
    // G[b].push_back(a);
  }
  rep(i, N) dfs(i);
  return 0;
}