class Solution(object):
    def reverse(self,s):
        return s[::-1]

    def reverseWords(self, s):
        """
        :type s: str
        :rtype: str
        """
        strs = s.split(' ')
        strs = map(self.reverse, strs)

        return ' '.join(strs)