

def isPalindrome(s:str):
    cleaned_s = [c.lower() for c in s if c.isalnum()]
    reversed_s = cleaned_s[::-1]
    return ''.join(cleaned_s) == ''.join(reversed_s)

print(isPalindrome('A man, a plan, a canal: Panama'))