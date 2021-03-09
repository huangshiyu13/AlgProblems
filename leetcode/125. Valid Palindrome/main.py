class Solution(object):
    def good(self, s):
        return s.isalnum()
    
    def isPalindrome(self, s):
        """
        :type s: str
        :rtype: bool
        """
        s = s.lower()
        i,j = 0, len(s)-1
        
        while i<j:
            while i < len(s) and not self.good(s[i]):
                i+=1
            if i >= j:
                break
            while j >=0 and not self.good(s[j]):
                j-=1
            
            if i<j:
                if not s[i] == s[j]:
                    return False
                i+=1
                j-=1
            else:
                break
        return True