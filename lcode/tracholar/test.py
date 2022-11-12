"""
给你一个未排序的整数数组，请你找出其中没有出现的最小的正整数，要求时间复杂度o(n)，空间复杂度o(1)
示例 1:
 输入: [1,2,0]
 输出: 3
 示例 2:
 输入: [3,4,-1,1]
 输出: 2
 示例 3:
 输入: [7,8,9,11,12]
 输出: 1
"""


def min_integer(arr):
    if arr is None or len(arr) == 0:
        return None

    for i in range(len(arr)):
        x = arr[i]
        arr[i] = None
        while x is not None and x < len(arr) and x > 0:
            z = arr[x]
            if z == x:
                break
            arr[x] = x
            arr[i] = None
            x = z

    for i in range(1, len(arr)):
        if arr[i] is None:
            return i

    return len(arr)


print(min_integer([1,2,0,1] ))
print(min_integer([3,4,-1,1]))
print(min_integer([7,8,9,11,12]))