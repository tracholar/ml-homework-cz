'''

# 删除一个元素使数组有序

问题： 给定一个由正整数数组，请按以下规则处理，使得数组有序（递增或者递减，不一定要严格递增或严格递减）：

- 数组已经是有序的，则不做处理，返回数组中最小的元素值。

- 如果数组不是有序的，

    - 若删除其中一个元素，使得剩余元素是有序的，返回需要删除的元素值；

    - 如果存在多个解，则选择删除元素值最小的。

    - 若无解，返回-1。

输入: N>1个整数，表示给定的数组，每个元素值的范围 [0, 200]。

输出: 一个整数，表示所求的返回值。



# 样例1

- 输入: 1 2

- 输出: 1

- 提示: 给定数组已经有序（递增），所以返回改数组的最小值 1 。

# 样例2

- 输入: 4 4 2 3 1

- 输出: 2

- 提示: 给定数组不是有序的，删除2后数组4 4 3 1是有序（递减）的，剔除3后数组4 4 2 1也是有序（递减）的，2和3都是可行的解，因为2比3小，因此返回 2 。

'''

class Solution:
    def is_order_list(self, nums):
        if len(nums) <= 2:
            return True
        sign = 0
        if nums[1] > nums[0]:
            sign = 1
        elif nums[1] < nums[0]:
            sign = -1
        before = nums[1]
        for x in nums[2:]:
            new_sign = x - before
            if new_sign > 0:
                new_sign = 1
            elif new_sign < 0:
                new_sign = -1
            before = x
            if sign == 0:
                sign = new_sign
            elif sign == new_sign or new_sign == 0:
                continue
            else:
                return False
        return True
    def sorted_by_del_one(self, nums):
        if nums is None or len(nums) == 0:
            return -1
        if len(nums) <= 2:
            return min(nums)
        del_item = -1
        sign = 0
        if nums[1] > nums[0]:
            sign = 1
        elif nums[1] < nums[0]:
            sign = -1
        before = nums[1]
        dp = [False] * len(nums)
        dp[0] = True
        dp[1] = True
        for i in range(2, len(nums)):
            new_sign = nums[i] - before
            if new_sign > 0:
                new_sign = 1
            elif new_sign < 0:
                new_sign = -1
            before = nums[i]
            if sign == 0:
                sign = new_sign
                dp[i] = dp[i-1]
            elif sign == new_sign or new_sign == 0:
                dp[i] = dp[i-1]
            else:
                dp[i] = False
                if dp[i-1]


            if :
                if del_item == -1 or del_item > nums[i]:
                    del_item = nums[i]

        return del_item

s = Solution()

assert (s.sorted_by_del_one([]) == -1)
assert (s.sorted_by_del_one([74]) == 74)
assert (s.sorted_by_del_one([1, 74]) == 1)
assert (s.sorted_by_del_one([3, 1, 2, 4]) == 3)
assert (s.sorted_by_del_one([3, 2, 6, 7]) == 2)
assert (s.sorted_by_del_one([1, 3, 2, 4]) == 2)
assert (s.sorted_by_del_one([1, 2, 5, 4]) == 4)
assert (s.sorted_by_del_one([1, 3, 2, 4, 4]) == 2)
assert (s.sorted_by_del_one([1, 2, 3, 2, 4, 4]) == 2)
assert (s.sorted_by_del_one([1, 3, 5, 3, 4]) == 5)
assert (s.sorted_by_del_one([4, 4, 6, 5, 1]) == -1)

assert (s.sorted_by_del_one([100, 74]) == 74)
assert (s.sorted_by_del_one([4, 2, 3, 1]) == 2)
assert (s.sorted_by_del_one([4, 4, 2, 3, 2]) == 2)
assert (s.sorted_by_del_one([10, 7, 3, 4]) == 3)

assert (s.sorted_by_del_one([11, 2, 8, 4]) == 2)