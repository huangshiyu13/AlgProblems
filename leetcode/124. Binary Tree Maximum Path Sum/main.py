# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution(object):
    def maxPathSum(self, root):
        self.max = None
        self.maxPath(root)
        return self.max

    def maxPath(self,node):
        if node == None:
            return 0
        l = max(0,self.maxPath(node.left))
        r = max(0,self.maxPath(node.right))
        if self.max == None or self.max < l+r+node.val:
            self.max = l+r+node.val
        return node.val+ max(l,r)

s = Solution()

root = TreeNode(2)
l = TreeNode(-1)
r = TreeNode(3)
root.left = l

print s.maxPathSum(root)