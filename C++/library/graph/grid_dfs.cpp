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
int H, W, sx, sy, h1, w1, ans;
string S;
string grid[3000];
bool visited[3000][3000];
vector<int> dh, dw;

bool dfs(int h, int w)
{
  rep(i, 4)
  {
    h1 = h + dh[i];
    w1 = w + dw[i];
    if (h1 >= H || h1 < 0 || w1 >= W || w1 < 0)
      continue;
    if (grid[h1][w1] == 'g')
    {
      return true;
    }
    if (grid[h1][w1] == '#')
      continue;
    if (visited[h1][w1])
      continue;
    visited[h1][w1] = true;
    if (dfs(h1, w1))
      return true;
  }
  return false;
}
int main()
{
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  cin >> H >> W;
  dh = {1, 0, -1, 0};
  dw = {0, 1, 0, -1};
  rep(h, H)
  {
    cin >> S;
    grid[h] = S;
    rep(w, W)
    {
      if (S[w] == 's')
      {
        sx = h;
        sy = w;
      }
    }
  }
  visited[sx][sy] = true;
  dfs(sx, sy);