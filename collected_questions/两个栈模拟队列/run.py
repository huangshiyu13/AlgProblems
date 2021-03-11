#!/usr/bin/python
# -*- coding: UTF-8 -*-

"""
@author: Shiyu Huang
@contact: huangsy1314@163.com
@file: question3.py
"""

class SuperQueue:
    def __init__(self,max_len=10):
        self.max_len = max_len
        self.InitQueue()

    def InitQueue(self):
        # 初始化
        self.stack1 = []
        self.stack2 = []
        return True

    def EnQueue(self, number):
        # 入队
        if len(self.stack1) < self.max_len:
            self.stack1.append(number)
            return True
        else:
            print('over size!')
            return False

    def DeQueue(self):
        # 出队
        if len(self.stack2) > 0:
            return self.stack2.pop()
        else:
            if len(self.stack1) > 0:
                while len(self.stack1) > 0:
                    self.stack2.append(self.stack1.pop())
                return self.stack2.pop()
            else:
                return None

    def IsEmptyQueue(self):
        # 判断是否为空
        return len(self.stack1) == 0 and len(self.stack2) == 0

def test_queue():
    # 测试一下下
    q = SuperQueue()
    for i in range(11):
        q.EnQueue(i)

    print(q.IsEmptyQueue())
    q.InitQueue()
    print(q.IsEmptyQueue())

    q.EnQueue(5)
    q.EnQueue(6)
    print(q.DeQueue())
    print(q.DeQueue())
    print(q.DeQueue())
    print(q.IsEmptyQueue())

if __name__ == '__main__':
    test_queue()