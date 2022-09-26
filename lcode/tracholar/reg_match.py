class Solution(object):

    def isMatch(self, s, p):
        """
        :type s: str
        :type p: str
        :rtype: bool
        """
        n = len(s)
        m = len(p)
        dp = [[False] * (m+1) for _ in range(n+1)]

        dp[0][0] = True
        if p[0] == '*':
            for i in range(1, n+1):
                dp[i][0] = True
        elif p[0] == '.' or p[0] == s[0]:
            dp[1][1] = True


        for i in range(1, n+1):
            for j in range(1, m+1):
                if p[j-1] == '.':
                    dp[i][j] = dp[i-1][j-1]
                elif p[j-1] == '*':
                    dp[i][j] = any(dp[x][j-1] for x in range(i))
                elif p[j-1] == s[i-1]:
                    dp[i][j] = dp[i-1][j-1]
                else:
                    dp[i][j] = False

        return dp[n][m]


s = Solution()
print(s.isMatch("aab", "c*a*b"))
