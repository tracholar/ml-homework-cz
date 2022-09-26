
class Solution(object):
    def majorityElement(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        target = 0
        for i in range(32):
            cnt = 0
            b = 1 << i
            for n in nums:
                if n & b > 0:
                    cnt += 1
            if cnt > len(nums)/2:
                target += b
        return target


s = Solution()
print(s.majorityElement([3,2,3]))