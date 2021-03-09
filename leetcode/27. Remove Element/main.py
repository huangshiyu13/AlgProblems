class Solution:
    def removeElement(self, nums, val):
        re_len = 0
        for num in nums:
            if num != val:
                nums[re_len] = num
                re_len+=1
        return re_len
        