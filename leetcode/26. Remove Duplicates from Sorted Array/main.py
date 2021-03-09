class Solution:
    def removeDuplicates_my(self, nums):
        nums_len = len(nums)
        if nums_len <= 1: return nums_len
        index_before = 0

        for i in range(1, nums_len):
            if nums[i] != nums[index_before]:
                index_before+=1
                nums[index_before] = nums[i]

        return index_before+1
    def removeDuplicates(self, nums):
        before_num = None
        re_len = 0
        for num in nums:
            if num != before_num:
                nums[re_len] = num
                before_num = num
                re_len+=1

        return re_len

nums = [1,1,2]

s = Solution()
n = s.removeDuplicates(nums)
print(nums[:n])
        