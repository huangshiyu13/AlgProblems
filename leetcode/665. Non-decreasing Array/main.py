min_value = -1e5
max_value = 1e5


class Solution:
    def checkPossibility(self, nums):
        wrongIndex = self.checkWrongIndex(
            nums)  # -1 for no, None for more than 2 wrong, else the position where is wrong
        if wrongIndex is None:
            return False
        if wrongIndex == -1 or wrongIndex == 0 or wrongIndex == len(nums) - 2:
            return True
        if nums[wrongIndex - 1] > nums[wrongIndex + 1] and nums[wrongIndex + 2] < nums[wrongIndex]:
            return False
        return True

    def checkWrongIndex(self, nums):
        wrong_indexes = []
        for i in range(len(nums) - 2, -1, -1):
            if nums[i] > nums[i + 1]:
                wrong_indexes.append(i)
            if len(wrong_indexes) > 1:
                return None
        if len(wrong_indexes) == 0:
            return -1
        else:
            return wrong_indexes[0]


if __name__ == '__main__':
    nums = [-1, 4, 2, 3]
    solution = Solution()
    print(solution.checkPossibility(nums))
