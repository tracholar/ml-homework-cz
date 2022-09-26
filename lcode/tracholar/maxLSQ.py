List = list

class Solution:
    def lengthOfLIS(self, nums: List[int], k: int) -> int:

        maxNum = [0]*(len(nums)+1)
        dp = [0]*(len(nums)+1)

        for i, n in enumerate(nums):
            i += 1

            maxLen = 0
            maxN = 0
            for j in range(i):
                if dp[j] == 0:
                    if maxLen <= 1:
                        maxLen = 1
                        maxN = n
                else:
                    if maxNum[j] < n and n - maxNum[j] <= k:
                        # 满足扩展条件
                        if maxLen < dp[j] + 1 or (maxLen == dp[j] + 1 and maxN > n):
                            maxLen = dp[j] + 1
                            maxN = n
                        else:
                            # 不扩展
                            pass
            maxNum[i] = maxN
            dp[i] = maxLen
        return max(dp)



s = Solution()
nums = [4,2,1,4,3,4,5,8,15]
k = 3
print(s.lengthOfLIS(nums, k))