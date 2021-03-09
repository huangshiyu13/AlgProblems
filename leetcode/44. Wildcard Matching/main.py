import collections

class Solution(object):
    def isMatch(self, s, p):
        self.p_original = p
        self.s_original = s
        return self._isMatch(s, p)

    def _isMatch(self,s, p, star = -1, ss = 0):
        ls = len(s)
        lp = len(p)

        if lp == 0:
            if ls == 0:
                return True
            if not star == -1:
                ss += 1
                return self._isMatch(self.s_original[ss:],self.p_original[star+1:],star,ss)
            return False

        c = p[0]
        if c == '?':
            return ls > 0 and self._isMatch(s[1:],p[1:],star,ss)
        if c == '*':
            t = 1
            while t < lp and p[t] == '*':
                t+=1
            p = p[t-1:]
            return self._isMatch(s,p[1:],len(self.p_original)-len(p),len(self.s_original)-len(s))

        if ls == 0:
            return False
        if s[0] == p[0]:
            return self._isMatch(s[1:],p[1:],star,ss)
        if not star == -1:
            ss += 1
            return self._isMatch(self.s_original[ss:],self.p_original[star+1:],star,ss)
        return False
        


s = Solution()
# source = "aaaabaabaabbbabaabaabbbbaabaaabaaabbabbbaaabbbbbbabababbaabbabbbbaababaaabbbababbbaabbbaabbaaabbbaabbbbbaaaabaaabaabbabbbaabababbaabbbabababbaabaaababbbbbabaababbbabbabaaaaaababbbbaabbbbaaababbbbaabbbbb"
# pattern = "**a*b*b**b*b****bb******b***babaab*ba*a*aaa***baa****b***bbbb*bbaa*a***a*a*****a*b*a*a**ba***aa*a**a*"
# source = "aa"
# pattern = '*'
# source =  "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
# pattern = "*aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa*"
# source = "aababbbbaaabaabaabbbbbaabbaabaaaabaaabbbaaaaabbbaaaabaaababbbbbbabbbabaababbbaaaaaaabaaaabbbaabbbaaabaaaababbababbaabaaaaabaaababbaababbabbbbabaabababbabbabbababbbbaaaabbbaabbaabbaabababbbbaaaabbabaaabbab"
# pattern = "*bbb*b*****a*abaab****a****b***a*ab*bb***b**bb*b*aab*aaa*a*b*bbbb*a*a*****ba**bb*b*****b*a*bb*******aa"
source ='aa'
pattern = '*'
print s.isMatch(source, pattern)