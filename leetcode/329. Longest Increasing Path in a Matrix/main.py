class Solution(object):
    def longestIncreasingPath(self, matrix):
        class Node():
            def __init__(self):
                self.pre = []
                self.val = None

        def buildGraph(matrix):
            ds = [[-1,0],[0,1],[1,0],[0, -1]]
            import collections
            dict = collections.defaultdict(Node)
            height = len(matrix)
            width = len(matrix[0])

            source = Node()
            target = Node()
            target.i = height
            target.j = width
            dict[(-1,-1)] = source
            dict[(height,width)] = target

            for i in range(height):
                for j in range(width):
                    dict[(i,j)].pre.append(source)
                    target.pre.append(dict[(i,j)])
                    for d in ds:
                        i_next = i+d[0]
                        j_next = j+d[1]
                        if i_next>= 0 and j_next >= 0 and i_next < height and j_next < width and matrix[i_next][j_next] > matrix[i][j]:
                            dict[(i,j)].pre.append(dict[(i_next,j_next)])
            return target

        def dp(node):
            if not node.pre:
                return 0
            if not node.val: node.val = 1+max(dp(i) for i in node.pre)
            return node.val
        if not matrix: return 0
        if not matrix[0]: return 0
        return dp(buildGraph(matrix))-1

nums = [[0,1,2,3,4,5,6,7,8,9],[19,18,17,16,15,14,13,12,11,10],[20,21,22,23,24,25,26,27,28,29],[39,38,37,36,35,34,33,32,31,30],[40,41,42,43,44,45,46,47,48,49],[59,58,57,56,55,54,53,52,51,50],[60,61,62,63,64,65,66,67,68,69],[79,78,77,76,75,74,73,72,71,70],[80,81,82,83,84,85,86,87,88,89],[99,98,97,96,95,94,93,92,91,90],[100,101,102,103,104,105,106,107,108,109],[119,118,117,116,115,114,113,112,111,110],[120,121,122,123,124,125,126,127,128,129],[139,138,137,136,135,134,133,132,131,130],[0,0,0,0,0,0,0,0,0,0]]

s = Solution()
print s.longestIncreasingPath(nums)