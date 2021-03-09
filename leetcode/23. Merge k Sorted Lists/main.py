# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution(object):
    def mergeKLists(self, lists):
        head = ListNode(None)
        lists = [ i for i in lists if i]
        import heapq
        heap = []
        for h in lists:
            heapq.heappush(heap,(h.val, h))

        headNow = head
        while heap:
            val, node = heapq.heappop(heap)
            headNow.next = node
            nextNode = node.next
            if nextNode:
                heapq.heappush(heap,(nextNode.val, nextNode))
            headNow = node

        return head.next

s = Solution()
h1 = ListNode(1)
print s.mergeKLists([h1]).val


# import Queue
# class ComparableObj:
#     def __init__(self, **):
      
#     def __cmp__(self, other):         
#         
#         return True/Flase
#         
# que = Queue.PriorityQueue()
# que.put(ComparableObj(**))
# que.put(ComparableObj(**))
# que.qsize()
# que.get()
