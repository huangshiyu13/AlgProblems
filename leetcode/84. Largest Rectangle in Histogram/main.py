class Solution(object):
    def largestRectangleArea(self, heights):
        heights.append(-1)
        stack = [(0,-1)]
        maxArea = -1
        for i,h in enumerate(heights):
            index0 = i
            while stack and stack[-1][0] > h:
                h0, index0 = stack.pop()
                area0 = h0*(i-index0)
                if area0 > maxArea:
                    maxArea = area0
            stack.append((h,index0))
        return maxArea

s = Solution()
heights = [2,1,2]
print s.largestRectangleArea(heights)
