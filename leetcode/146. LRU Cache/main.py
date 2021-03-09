class Node():
    key = 0
    value = 0
    pre = None
    post = None

class LRUCache(object):

    def __init__(self, capacity):
        """
        :type capacity: int
        """
        self.remind = capacity
        self.head = Node()
        self.tail = Node()

        self.head.post = self.tail
        self.tail.pre = self.head
        self.dic = {}
        self.count = 0

    def get(self, key):
        """
        :type key: int
        :rtype: int
        """
        if not self.dic.has_key(key):
            return -1

        node = self.dic[key]
        self.remove(node)
        self.add(node)
        return node.value



    def put(self, key, value):
        """
        :type key: int
        :type value: int
        :rtype: void
        """
        if self.dic.has_key(key):
            node = self.dic[key]
            node.value = value
            self.remove(node)
        else:
            node = Node()
            node.value = value
            node.key = key
            self.dic[key] = node

        self.add(node)

        if self.count > self.remind:
            tail_key = self.tail.pre.key
            del self.dic[tail_key]
            self.remove(self.tail.pre)

    def remove(self, node):
        pre = node.pre
        post = node.post

        pre.post = post
        post.pre = pre

        self.count -= 1

    def add(self, node):
        node.pre = self.head
        node.post = self.head.post

        self.head.post.pre = node
        self.head.post = node

        self.count += 1

l = LRUCache(2)

print l.get(1)
l.put(1,2)
print l.get(1)