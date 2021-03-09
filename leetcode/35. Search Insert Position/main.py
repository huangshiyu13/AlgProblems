class Solution:
    def searchInsert_my(self, nums, target):
        for num in nums:
            if num >= target:
                return nums.index(num)
        return len(nums)

    def searchInsert(self, nums, target):
        left = 0
        right = len(nums)
        while left < right:
            middle = (left+right)>>1
            middle_value = nums[middle]
            if middle_value == target:
                return middle
            else:
                if middle_value > target:
                    right = middle
                else:
                    left = middle+1

        return left
