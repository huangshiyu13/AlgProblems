class Solution(object):
    def split(self, a):
        a = a[:-1].split('+')

        return int(a[0]),int(a[1])

    def complexNumberMultiply(self, a, b):
        """
        :type a: str
        :type b: str
        :rtype: str
        """
        a1, a2 = self.split(a)
        b1, b2 = self.split(b)
        c1 = a1*b1-a2*b2
        c2 = a1*b2+a2*b1
        return str(c1)+'+'+str(c2)+'i'

s = Solution()
print s.complexNumberMultiply("1+1i","1+1i")