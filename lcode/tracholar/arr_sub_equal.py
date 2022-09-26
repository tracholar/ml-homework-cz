# coding:utf-8

def array_find(arr, s):
    # 找到和为s的子数组
    dp = [[False] * (s+1) for _ in arr]
    for i in range(len(arr)):
        dp[i][0] = True

    for i, v in enumerate(arr):
        if i == 0:
            dp[0][v] = True
            continue

        for j in range(1, s+1):
            if v > s:
                dp[i][j] = dp[i-1][j]
            else:
                dp[i][j] = dp[i-1][j] or dp[i-1][j-v]
    return dp[len(arr)-1][s]




arr = [1,2,5]
print(array_find(arr, 4))

