
class Solution(object):
    def superEggDrop(self, k, n):
        """
        :type k: int
        :type n: int
        :rtype: int
        """
        #   dp[k][n] =  1 + min(  max(dp[k-1][x], dp[k-1][n-x])  for x in 1,2,...,n)
        dp = [[0] * n for _ in range(k)]

        for x in range(n):
            dp[0][x] = x + 1
        for x in range(k):
            dp[x][0] = 1

        for i in range(1, k):
            for j in range(1, n):
                dp[i][j] = 1 + max(dp[i-1][1], dp[i][j-1])
                for x in range(1, j+1):
                    dp[i][j] =  min(dp[i][j], 1 + max(dp[i-1][x-1], dp[i][j-x]))

        return dp[k-1][n-1]

s = Solution()
print(s.superEggDrop(2, 2))