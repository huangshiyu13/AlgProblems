class Solution(object):
    def countBits(self, num):
        """
        :type num: int
        :rtype: List[int]
        """
        re = [0]
        while len(re) < num+1:
            re.extend([x+1 for x in re])

        return re[:num+1]