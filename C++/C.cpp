// g++ A.cpp -std=c++14 -I . && ./a.out
#include <bits/stdc++.h>
using namespace std;
#include <atcoder/all>
using namespace atcoder;
// using mint = modint1000000007;
using mint = modint998244353;
#define rep(i, n) for (int i = 0; i < (int)(n); i++)
#define rep2(i, a, b) for (int i = a; i < (int)(b); i++)
#define rrep(i, a, b) for (int i = a; i > (int)(b); i--)
#define all(v) v.begin(), v.end()
using ll = long long;
const ll INF = 1e18;
// 変数定義
ll N, M, K, a, b, c, d, e, x, y, t, T, total, cnt;
int k;
mint ans;
int main()
{
  ios::sync_with_stdio(false);
  cin.tie(nullptr);
  cin >> N >> K;
  vector<vector<mint>> dp(N + 1, vector<mint>(N + 1, mint(0)));
  dp[0][0] = mint(1);
  rep2(i, 1, N + 1)
  {
    rep2(j, 1, N + 1)
    {
      k = j - 1;
      while (k <= N)
      {
        dp[i][j] += dp[i - 1][k];
        k = k * 2 + 1;
      }
    }
  }
  ans = dp[N][K];
  cout << ans.val() << '\n';
  return 0;
}