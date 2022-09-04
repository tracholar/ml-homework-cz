
class Solution(object):
    def lengthOfLongestSubstring(self, s):
        """
        :type s: str
        :rtype: int
        """
        s_array = list(s)

        max_len = 0
        cur_len = 0
        max_char = []
        for c in s_array:
            if c not in max_char:
                cur_len += 1
                max_char.append(c)
            else:

                # 找到以c结尾的当前最长子串
                j = len(max_char) - 1
                while max_char[j] != c:
                    j -= 1
                max_char = max_char[j+1:]
                max_char.append(c)
                cur_len = len(max_char)

            if max_len < cur_len:
                max_len = cur_len
        return max_len


s = Solution()
print(s.lengthOfLongestSubstring("abcabcbb"))