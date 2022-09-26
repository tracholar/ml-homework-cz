
price = [0, 1, 5,8,9,10,17,17,20,24,30]

def max_amount(n):
    dp = [0] * (n+1)

    #dp[n] = max(dp[n-k] + price[k] for k in (1,10))
    for i in range(1, n + 1):
        dp[i] = 0
        for k in range(1, 11):
            if i - k >= 0:
                dp[i] = max(dp[i], dp[i-k] + price[k])
    return dp[n]

print('n max_amout')
for i in range(1, 11):
    print(i, max_amount(i))