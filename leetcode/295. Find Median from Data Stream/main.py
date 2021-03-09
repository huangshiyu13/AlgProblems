from heapq import heappush, heappop
class MedianFinder(object):

    def __init__(self):
        """
        initialize your data structure here.
        """
        self.maxheap = []
        self.minheap = []
        self.count = 0

    def addNum(self, num):
        """
        :type num: int
        :rtype: void
        """
        if not self.maxheap:
            heappush(self.maxheap, -num)
            self.count += 1
            return

        if self.count % 2 == 1:
            tmp = -heappop(self.maxheap)
            minv, maxv = min(tmp, num), max(tmp, num)
            heappush(self.maxheap, -minv)
            heappush(self.minheap, maxv)
        else:
            tmp = heappop(self.minheap)
            minv, maxv = min(tmp, num), max(tmp, num)
            heappush(self.maxheap, -minv)
            heappush(self.minheap, maxv)

        self.count += 1

    def findMedian(self):
        """
        :rtype: float
        """
        if self.count % 2 == 1:
            return float(-self.maxheap[0])
        return (-self.maxheap[0]+self.minheap[0])/2.


# Your MedianFinder object will be instantiated and called as such:
obj = MedianFinder()
obj.addNum(1)
obj.addNum(2)
obj.addNum(3)
print obj.maxheap
print obj.findMedian()
print heappop(obj.maxheap)