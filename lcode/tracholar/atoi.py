
class Solution(object):
    def is_number(self, c):
        return ord(c) >= ord('0') and ord(c) <= ord('9')

    def myAtoi(self, s):
        """
        :type s: str
        :rtype: int
        """
        number = 0
        sign = 1
        for c in s:
            if c == '-':
                sign = -1
            elif self.is_number(c):
                number = number*10 + int(c)
        number = number * sign
        if number < - pow(2, 31):
            number = -pow(2, 31)
        elif number > pow(2, 31)-1:
            number = pow(2, 31)-1
        return number

s = 'adfadfasdf'
print(ord(s[2]))
print(ord('A'))
print(chr(54))
s = Solution()
print(s.myAtoi('djfasdjfl345345'))

