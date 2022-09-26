
class Solution(object):
    def concat(self, a, b):
        z = []
        for x in a:
            for y in b:
                z.append(x + y)
        return z

    def generateParenthesis(self, n):
        """
        :type n: int
        :rtype: List[str]
        """

        if n == 1:
            return ['()']
        r = []

        for i in range(1, n):
            list1 = ['(' + c + ')' for c in self.generateParenthesis(n-1)]
            list2 = self.concat(self.generateParenthesis(i), self.generateParenthesis(n-i))
            r = r + list1 + list2
        return r


s = Solution()
print(s.generateParenthesis(2))
