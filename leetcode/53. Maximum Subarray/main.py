class Solution:
    def maxSubArray(self, nums):
        if len(nums) == 0 : return 0
        max_sum = nums[0]
        sum_now = 0
        for num in nums:
            sum_now += num
            if sum_now>max_sum:
                    max_sum = sum_now
            if sum_now < 0:
                sum_now=0
                
        return max_sum
        