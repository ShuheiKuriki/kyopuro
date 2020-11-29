// g++ E.cpp -std=c++14 -I . && ./a.out
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
ll H, W, a, b, c, d, x, y, t, T, total, cnt, ans;
int grid_bfs(vector<string> &s)
{
  const int vx[] = {0, 1, 0, -1}, vy[] = {1, 0, -1, 0};
  vector<vector<int>> min_cost(s.size(), vector<int>(s[0].size(), -1));
  queue<pair<int, int>> que;
  pair<int, int> goal;
  for (int i = 0; i < s.size(); i++)
  {
    for (int j = 0; j < s[i].size(); j++)
    {
      if (s[i][j] == 'S')
      {
        que.emplace(i, j);
        min_cost[i][j] = 0;
      }
      if (s[i][j] == 'G')
      {
        goal = make_pair(i, j);
      }
    }
  }
  while (!que.empty())
  {
    auto p = que.front();
    que.pop();
    for (int i = 0; i < 4; i++)
    {
      int ny = p.first + vy[i], nx = p.second + vx[i];
      if (nx < 0 || ny < 0 || nx >= s[0].size() || ny >= s.size())
        continue;
      if (min_cost[ny][nx] != -1)
        continue;
      if (s[ny][nx] == '#')
        continue;
      min_cost[ny][nx] = min_cost[p.first][p.second] + 1;
      if (make_pair(ny, nx) == goal)
        return min_cost[ny][nx];
      que.emplace(ny, nx);
    }
  }
  return -1;
}
int main()
{
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  cin >> H >> W;
  vector<string> grid(H);
  rep(i, H) cin >> grid[i];
  cout << grid_bfs(grid) << '\n';
  return 0;
}
