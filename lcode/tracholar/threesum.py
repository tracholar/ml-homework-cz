class Solution(object):

    def threeSum(self, nums):
        """
        :type nums: List[int]
        :rtype: List[List[int]]
        """
        if len(nums) < 3:
            return []
        nums.sort()

        r = []
        k = 1
        while k > 0 and k < len(nums)-1:
            i,j = 0, len(nums)-1
            while i < k and j > k:
                s = nums[i] + nums[j] + nums[k]

                if s == 0:
                    r.append((nums[i], nums[k], nums[j]))

                    i += 1
                    j -= 1
                    continue

                if s < 0:
                    i += 1
                else:
                    j -= 1
            k += 1
        r = list(list(x) for x in set(r))
        return r

s = Solution()
nums = [3,0,-2,-1,1,2]
print(s.threeSum(nums))