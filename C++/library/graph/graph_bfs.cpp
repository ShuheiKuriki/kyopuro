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
const ll INF = 1e18;
// 変数定義
ll N, M, Q, a, b, c, d, x, y, t, T, total, cnt, ans;
int main()
{
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  cin >> N >> M;
  vector<vector<int>> edge(N);
  rep(i, M)
  {
    int u, v;
    cin >> u >> v;
    edge[u - 1].push_back(v - 1);
    edge[v - 1].push_back(u - 1);
  }
  queue<int> que;
  vector<int> min_cost(N, -1);
  int start = 0;
  que.push(start);
  min_cost[start] = 0;
  while (que.size())
  {
    int v = que.front();
    que.pop();
    for (auto w : edge[v])
    {
      if (min_cost[w] == -1)
      {
        min_cost[w] = min_cost[v] + 1;
        que.push(w);
      }
    }
  }
  return 0;
}