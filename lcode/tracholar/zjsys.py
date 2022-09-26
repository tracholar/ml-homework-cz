
"""
2 2
2 4 1 5
"""

def shuffle_op(arr):
    if len(arr) <= 1:
        return arr

    n = len(arr)
    mid = n // 2
    left = shuffle_op(arr[:mid])
    right = shuffle_op(arr[mid:])
    return right + left

n, t = [int(x) for x in input().strip().split(' ', 2)]
arr = [int(x) for x in input().strip().split(' ') if len(x) > 0]

for _ in range(t):
    arr = shuffle_op(arr)

print(' '.join(str(x) for x in arr))
