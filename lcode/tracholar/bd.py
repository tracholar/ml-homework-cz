import numpy as np


def solution(A, m, n, k):
    dp = [[-np.inf] * (m + 1) for _ in range(n + 1)]
    dp[0][0] = 0

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            dp[i][j] = dp[i - 1][j]
            for z in range(1, k + 1):
                if j - k >= 0:
                    dp[i][j] = max(dp[i][j], dp[i - 1][j - k] + A[j - 1])

    return max(dp[n])


A = [1, 4, 6, 7, 8, 9, 2, 4, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 100]
m = len(A)
n = 4
k = 3

print(solution(A, m, n, k))
