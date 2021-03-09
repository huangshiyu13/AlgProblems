class Solution(object):
    def maxSlidingWindow(self, nums, k):
        deque = []
        re = []
        for i,n in enumerate(nums):
            if deque and i-deque[0] >= k:
                deque.pop(0)
            while deque and nums[deque[-1]] < n:
                deque.pop()
            deque.append(i)
            if i+1 >= k:
                re.append(nums[deque[0]])
        return re

s = Solution()
print s.maxSlidingWindow([3,2,1,4,5],3)
