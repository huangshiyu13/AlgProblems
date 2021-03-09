# https://www.cnblogs.com/cotyb/archive/2016/02/11/5186461.html
# https://www.cnblogs.com/graphics/archive/2010/06/21/1752421.html
class Solution(object):
    def hammingDistance(self, x, y):
        """
        :type x: int
        :type y: int
        :rtype: int
        """
        return bin(x^y).count('1')


s = Solution()
print s.hammingDistance(1,4)