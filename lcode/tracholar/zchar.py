class Solution(object):
    def convert(self, s, numRows):
        """
        :type s: str
        :type numRows: int
        :rtype: str
        """
        if numRows < 2:
            return s
        results = []
        for _ in range(numRows):
            results.append([])
        i = 0
        flag = 1
        for c in s:
            results[i].append(c)

            if i == numRows-1:
                flag = -1
            elif i == 0 :
                flag = 1

            i += flag

        print(results)
        return ''.join(''.join(c) for c in results)

s = Solution()
print(s.convert('ABC', 1))