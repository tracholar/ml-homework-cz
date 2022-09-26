class Solution(object):

    def candy(self, ratings):
        """
        :type ratings: List[int]
        :rtype: int
        """

        candyNums = [1]*len(ratings)
        pre = ratings[0]
        for i in range(1, len(ratings)):
            if ratings[i] > pre:
                candyNums[i] = candyNums[i-1] + 1
            else:
                candyNums[i] = 1
            pre = ratings[i]

        pre = ratings[-1]
        for i in list(range(0, len(ratings)-1))[::-1]:
            if ratings[i] > pre:
                candyNums[i] = max(candyNums[i+1] + 1, candyNums[i])
            else:
                pass
            pre = ratings[i]

        return sum(candyNums)



s = Solution()
print(s.candy([1,3,4,5,2]))