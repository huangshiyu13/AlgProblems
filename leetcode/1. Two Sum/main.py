
class Num:
    def __init__(self, index,value):
        self.index = index
        self.value = value

class Solution:
    def twoSum_my(self, nums, target):
        nums_dict = [Num(index,value) for index,value in enumerate(nums)]
        nums_dict.sort(key=lambda n:n.value)
        start_index = 0
        end_index = len(nums)-1
        assert end_index-start_index>=1
        while start_index<end_index:
            value_now = nums_dict[start_index].value+nums_dict[end_index].value
            if  value_now == target:
                return [nums_dict[start_index].index,nums_dict[end_index].index]
            else:
                if value_now < target:
                    start_index+=1
                else:
                    end_index-=1

    def twoSum(self, nums, target):
        memory = {}
        for i in range(len(nums)):
            t = target-nums[i]
            if t in memory:
                return [i,memory[t]]
            else:
                memory[nums[i]] = i


nums  = [1,9]
target = 10

s = Solution()
print(s.twoSum(nums,target))