from collections import Counter

class Solution(object):
    def judgeCircle(self, moves):
        """
        :type moves: str
        :rtype: bool
        """
        c = Counter(moves)
        return c['U'] == c['D'] and c['L'] == c['R']

s = Solution()
strs = 'UL'
print s.judgeCircle(strs)