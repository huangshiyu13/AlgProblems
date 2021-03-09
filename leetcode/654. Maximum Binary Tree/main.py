# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution(object):

    def constructMaximumBinaryTree(self, nums):
        """
        :type nums: List[int]
        :rtype: TreeNode
        """
        firstNode = TreeNode(nums[0])
        if len(nums) == 1:
            return firstNode

        stack = []
        stack.append(firstNode)

        for i in nums[1:]:
            nodeNow = TreeNode(i)
            popBefore = None
            while stack and stack[-1].val < i:
                popNode = stack.pop()
                popNode.right = popBefore
                popBefore = popNode

            nodeNow.left = popBefore
            stack.append(nodeNow)

        while stack:
            popNode = stack.pop()
            if stack: stack[-1].right = popNode
        return popNode


a = [3,2,1,6,0,5]
s = Solution()
b = s.constructMaximumBinaryTree(a)
print b.val