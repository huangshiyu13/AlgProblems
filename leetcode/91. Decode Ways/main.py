import collections

class Solution(object):

    def numDecodings(self, s):
        """
        :type s: str
        :rtype: int
        """
        if len(s) == 0: return 0
        self.dict = collections.defaultdict(int)
        return self._numDecodings(s , -1)

    def _numDecodings(self, s, pre):
        if len(s) == 0:
            if pre == -1:
                return 1
            return 0
        
        if pre == -1:
            preNext = int(s[0])
            if preNext == 0:
                return 0
            
            if preNext < 3:
                if self.dict.has_key((s,pre)): 
                    return self.dict[(s,pre)]
                else:
                    re = self._numDecodings(s[1:], preNext)+ self._numDecodings(s[1:], -1)
                    self.dict[(s,pre)] = re
                    return re
            
            if self.dict.has_key((s,pre)): 
                return self.dict[(s,pre)]
            else:
                re = self._numDecodings(s[1:],-1)
                self.dict[(s,pre)] = re
                return re
       
        if pre == 2 and int(s[0]) > 6:
            return 0
        
        if self.dict.has_key((s,pre)): 
            return self.dict[(s,pre)]
        else:
            re = self._numDecodings(s[1:],-1)
            self.dict[(s,pre)] = re
            return re

s = Solution()
print s.numDecodings("110")


