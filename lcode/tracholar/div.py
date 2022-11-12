class Solution(object):

    def findMaxMultipy(self, dividend, divisor):
        z = 0
        n = 0
        max_divisor = divisor
        while divisor <= dividend:
            if z == 0:
                z = 1
            else:
                z = z << 1
            n += 1

            max_divisor = divisor
            divisor = divisor << 1
        return z, n, max_divisor

    def _divide(self, dividend, divisor):
        if dividend < 0:
            return -self._divide(-dividend, divisor)
        if divisor < 0:
            return -self._divide(dividend, -divisor)

        if divisor > dividend:
            return 0

        result = 0
        while dividend >= divisor:
            z, n, to_minus = self.findMaxMultipy(dividend, divisor)
            result += z
            dividend -= to_minus

        return result

    def divide(self, dividend, divisor):
        """
        :type dividend: int
        :type divisor: int
        :rtype: int
        """

        if (dividend < 0 and divisor > 0) or \
                (dividend > 0 and divisor < 0) :
            return max(-2**31, self._divide(dividend, divisor))
        else:
            return min(2**31-1, self._divide(dividend, divisor))





s = Solution()
print(s.divide(-2147483648, 1))
