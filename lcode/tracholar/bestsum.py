class Solution(object):
    def threeSumClosest(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: int
        """
        nums.sort()
        bestSum = None
        bestDiff = None
        for i,n in enumerate(nums):
            if i in (0, len(nums)-1):
                continue

            j, k = 0, len(nums) - 1

            while j < i and i < k:
                s = nums[i] + nums[j] + nums[k]
                diff = abs(target - s)

                if diff == 0:
                    return target

                if bestSum is None or bestDiff > diff:
                    bestDiff = diff
                    bestSum = s

                if target < s:
                    k -= 1
                else:
                    j += 1

        return bestSum

s = Solution()
nums = [-1,2,1,-4]
target = 1
r = s.threeSumClosest(nums, target)
print(r)