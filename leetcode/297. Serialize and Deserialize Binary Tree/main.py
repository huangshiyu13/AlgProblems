# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Codec:
    def serialize(self, root):
        """Encodes a tree to a single string.

        :type root: TreeNode
        :rtype: str
        """
        re = []

        def preorder(node):
            if not node:
                re.append('#')
            else:
                re.append(str(node.val))
                preorder(node.left)
                preorder(node.right)

        preorder(root)

        return ' '.join(re)



    def deserialize(self, data):
        """Decodes your encoded data to tree.

        :type data: str
        :rtype: TreeNode
        """
        strList = data.split(' ')

        def decode():
            val = strList[0]
            strList.pop(0)
            if val == '#':
                return None
            node = TreeNode(int(val))
            node.left = decode()
            node.right = decode()
            return node

        return decode()

# Your Codec object will be instantiated and called as such:
codec = Codec()

root = TreeNode(1)
l = TreeNode(2)
r = TreeNode(3)
root.left = l
root.right = r
# root = None

str1 = codec.serialize(root)
print str1
root =  codec.deserialize(str1)
print root.val, root.left.val, root.right.val