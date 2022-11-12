class Solution(object):
    def searchRange(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """

        n = len(nums)
        i,j = 0, n-1

        while i <= j:
            mid = (i + j) // 2

            if nums[mid] > target:
                i, j = i, mid-1
            elif nums[mid] < target:
                i, j = mid + 1, j
            else:
                i, j = mid, mid
                while i-1>=0 and nums[i-1] == target:
                    i -= 1
                while j+1<len(nums) and nums[j+1] == target:
                    j += 1

                return [i, j]

        return [-1, -1]

s = Solution()
print(s.searchRange([1,1,2], 1))
