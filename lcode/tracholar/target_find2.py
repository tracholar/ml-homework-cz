
class Solution(object):
    def binSearchLeft(self, nums, target):
        n = len(nums)
        i, j = 0, n-1

        while i < j:
            mid = (j+i)//2
            if nums[mid] > target:
                j = mid - 1
            elif nums[mid] < target:
                i = mid + 1
            else:
                # 相等
                if mid-1>=0 and nums[mid-1] == target:
                    j = mid - 1
                else:
                    return mid
        if i == j and nums[i] == target:
            return i
        return -1

    def binSearchRight(self, nums, target):
        n = len(nums)
        i, j = 0, n-1

        while i < j:
            mid = (j+i)//2
            if nums[mid] > target:
                j = mid - 1
            elif nums[mid] < target:
                i = mid + 1
            else:
                # 相等
                if mid+1<n and nums[mid+1] == target:
                    i = mid + 1
                else:
                    return mid
        if i == j and nums[i] == target:
            return i
        return -1


    def searchRange(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        return [
            self.binSearchLeft(nums, target),
            self.binSearchRight(nums, target)
        ]




s = Solution()
print(s.searchRange([1,1,1,1,2], 1))
