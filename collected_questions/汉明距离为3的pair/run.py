import time

str_f = {5:'{:05b}',16:'{:016b}',32:'{:032b}',64:'{:064b}'}
str_index = 16

def hammingDistance(x, y):
    """
    :type x: int
    :type y: int
    :rtype: int
    """
    return bin(x ^ y).count('1')
#

class Solution1(object): #暴力算法，对列表里面的数据进行两两比较，算法复杂度为O(n^2)
    def solve_single(self,data):
        re = set()
        for i in range(len(data)-1):
            for j in range(i+1,len(data)):
                x = data[i]
                y = data[j]
                if hammingDistance(x,y) == 3:
                    li = [x,y] if x<y else [y,x]
                    li = [str_f[str_index].format(ll) for ll in li]
                    re.add(','.join(li) )
        re = list(re)
        re.sort()
        return re

    def solve(self,data):
        re = []
        for data0 in data:
            re.append(self.solve_single(data0))
        return re


def span(data):
    re = []
    index_tmp = 1
    for i in range(str_index):
        re.append(data^index_tmp)
        index_tmp =index_tmp<<1
    return re

class Solution2(object): # 线性算法，算法复杂度为O(m^2*n),m为数据的长度，n为数据的个数
    def solve_single(self,data):
        re = set()
        check_list = set()
        before_list = {}
        for data0 in data:
            one_span = span(data0)
            check_list.update(one_span)
            for s0 in one_span:
                if s0 in before_list:
                    before_list[s0].add(data0)
                else:
                    before_list[s0]={data0}

        for item in check_list:
            spaned = span(item)
            for spaned_item in spaned:
                if spaned_item in check_list:
                    xs = before_list[spaned_item]
                    ys = before_list[item]
                    for x in xs:
                        for y in ys:
                            if hammingDistance(x,y) == 3:
                                li = [x, y] if x < y else [y, x]
                                li = [str_f[str_index].format(ll) for ll in li]
                                re.add(','.join(li))
        re = list(re)
        re.sort()
        return re

    def solve(self,data):
        re = []
        for data0 in data:
            re.append(self.solve_single(data0))
        return re

def re_check(re1,re2):
    return re1 == re2

if __name__ == '__main__':
    with open('data.txt', 'r') as f:
        data = [ eval(line.strip()) for line in f.readlines()]
        data = [[int(s, 2) for s in line] for line in data]
    solution1 = Solution1()
    solution2 = Solution2()

    s_t = time.time()
    re1 = solution1.solve(data)
    use_t = time.time()-s_t
    print('use time {}'.format(use_t))

    s_t = time.time()
    re2 = solution2.solve(data)
    use_t = time.time() - s_t
    print('use time {}'.format(use_t))

    print(re_check(re1,re2))


