class Solution(object):
    def arrayPairSum(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        # nums.sort()
        # re = 0
        # for i in range(0,len(nums),2):
        #     re += nums[i]
        # return re

        # count = [0]*20001
        # for i in nums:
        #     count[i+10000] += 1

        # re = 0
        # flag = 0
        # for i,c in enumerate(count):
        #     cNow = c-1 if flag else c
        #     if cNow&1 == 1:
        #         re += (cNow//2+1)*(i-10000)
        #         flag = 1
        #     else:
        #         re += (cNow//2)*(i-10000)
        #         flag = 0
        # return re

        count = [0]*20001
        for i in nums:
            count[i+10000] += 1

        re = 0
        flag = True
        for i,c in enumerate(count):
            while c > 0:
                if flag:
                    re+=i-10000
                flag = not flag
                c -= 1
        return re


s = Solution()
print s.arrayPairSum([1,4,3,2])