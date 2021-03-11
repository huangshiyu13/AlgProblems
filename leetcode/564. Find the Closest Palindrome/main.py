def re_check(re1, re2):
    return re1 == re2


def check_palindrome(n):
    """
        :type n: str
        :rtype: bool
    """
    i = 0
    j = len(n) - 1
    while i < j:
        if n[i] != n[j]:
            return False
        i += 1
        j -= 1
    return True


def check_palindrome_int(n):
    """
        :type n: int
        :rtype: bool
    """
    n = str(n)
    return check_palindrome(n)


class Solution1:
    def nearestPalindromic(self, n: str) -> str:
        if n == '0':
            return '1'

        n = int(n)
        i = 1
        while True:
            next_n = n - i
            # print(next_n)
            if check_palindrome_int(next_n):
                return str(next_n)
            next_n = n + i
            # print(next_n)
            if check_palindrome_int(next_n):
                return str(next_n)
            i += 1


def cand1(n):  # 得到降位数的最近
    n_len = len(n)
    if n[0] == '1':
        return '9' * (n_len - 1)
    else:
        first = str(int(n[0]) - 1)
        if n_len <= 1:
            return first
        else:
            return first + '9' * (n_len - 2) + first


def cand2(n):  # 得到升位数的最近
    n_len = len(n)
    if n[0] == '9':
        return '1' + '0' * (n_len - 1) + '1'
    else:
        first = str(int(n[0]) + 1)
        if n_len <= 1:
            return first
        else:
            return first + '0' * (n_len - 2) + first


def cand1_fixed(n):  # 得到降位数的最近,位数不变
    n_len = len(n)
    if n[0] == '0':
        return None
    else:
        first = str(int(n[0]) - 1)
        if n_len <= 1:
            return first
        else:
            return first + '9' * (n_len - 2) + first


def cand2_fixed(n):  # 得到升位数的最近,位数不变
    n_len = len(n)
    if n[0] == '9':
        return None
    else:
        first = str(int(n[0]) + 1)
        if n_len <= 1:
            return first
        else:
            return first + '0' * (n_len - 2) + first


def re_find(n):  # 找到离n最近的回文数，包括自身，长度不变
    if len(n) <= 1 or check_palindrome(n):  # 如果是位数小于等于1，或者本身为回文数，则直接返回
        return n
    else:  # 如本身不是回文数，则返回不包含自身的回文数
        return re_find_except(n)


def re_find_except(n):  # 找到离n最近的回文数，不包括自身，长度不变
    if len(n) < 1:  # 如果是位数小于1，则直接返回就行
        return None

    n_int = int(n)
    cand_list = []
    re = cand1_fixed(n)
    if not re is None:
        cand_list.append(re)  # 得到降位数的最近

    re = cand2_fixed(n)
    if not re is None:
        cand_list.append(re)  # 得到升位数的最近

    if not check_palindrome(n):  # 如果本身不为回文数，找到的回文数肯定不包含自身
        re = cand3_no_except(n)
        if not re is None:
            cand_list.append(re)  # 得到不升位数不降位数的最近,包含自身
    else:
        re = cand3(n)
        if not re is None:
            cand_list.append(re)  # 得到不升位数不降位数的最近,不包含自身
    # for c in cand_list:
    #     print(c)
    # exit()
    if len(cand_list) == 0:
        return None

    min_dur = None
    min_re = None

    for cand_n in cand_list:
        if cand_n is None:
            continue
        dur_tmp = abs(int(cand_n) - n_int)

        if min_dur is None or dur_tmp < min_dur or (dur_tmp == min_dur and int(cand_n) < int(min_re)):
            min_re = cand_n
            min_dur = dur_tmp
    return min_re


def cand3_no_except(n):  # 得到首数字不变的,包含本身的回文数
    if check_palindrome(n):  # 如果本身是个回文数,直接返回
        return n
    else:  # 如果本身不是个回文数，递归找中间最近的回文就可以了
        if len(n) == 2:
            return n[0] * 2
        if n[0] == n[-1]:
            # print(n[1:-1],re_find(n[1:-1]))
            return n[0] + re_find(n[1:-1]) + n[0]
        else:
            to_find_value = int(n[1:-1])
            inner_dis_value = abs(int(re_find(n[1:-1])) - to_find_value)
            # print(n[1:-1], re_find(n[1:-1]), inner_dis_value)
            # exit()
            # print(inner_dis_value)
            values = []
            for ii in range(0, 11):
                values += [to_find_value - inner_dis_value + ii, to_find_value - inner_dis_value - ii,
                           to_find_value + inner_dis_value + ii, to_find_value + inner_dis_value - ii]

            best_re = None
            best_dis = None
            for value in values:
                if value < 0 or len(str(value)) > len(n[1:-1]):
                    continue
                value = '0' * (len(n[1:-1]) - len(str(value))) + str(value)

                if not check_palindrome(value):
                    continue
                tmp_re = n[0] + value + n[0]
                tmp_dis = abs(int(tmp_re) - int(n))
                # print(n,tmp_re,tmp_dis)
                if best_dis is None or tmp_dis < best_dis or (tmp_dis == best_dis and tmp_re < best_re):
                    best_re = tmp_re
                    best_dis = tmp_dis

            return best_re


def cand3(n):  # 得到首数字不变的,不包含本身的回文数

    if check_palindrome(n):  # 如果本身是个回文数,需要在中间最近找不包含本身的回文数
        if len(n) <= 2:  # 如果n是回文数，且位数小于等于2，则不存在首字母一样的回文数
            return None
        re = re_find_except(n[1:-1])

        if re is None:
            return None
        else:
            return n[0] + re + n[0]

    else:  # 如果本身不是个回文数，递归找中间回文就可以了
        if len(n) == 2:
            return n[0] * 2

        if n[0] == n[-1]:
            # print(n[1:-1],re_find(n[1:-1]))
            return n[0] + re_find(n[1:-1]) + n[0]
        else:
            # return n[0] + re_find(n[1:-1]) + n[0]
            to_find_value = int(n[1:-1])
            inner_dis_value = abs(int(re_find(n[1:-1])) - to_find_value)
            # print(n[1:-1],re_find(n[1:-1]),inner_dis_value)
            # exit()
            # print(inner_dis_value)
            values = []
            for ii in range(0, 11):
                values += [to_find_value - inner_dis_value + ii, to_find_value - inner_dis_value - ii,
                           to_find_value + inner_dis_value + ii, to_find_value + inner_dis_value - ii]

            best_re = None
            best_dis = None
            for value in values:
                if value < 0 or len(str(value)) > len(n[1:-1]):
                    continue
                value = '0' * (len(n[1:-1]) - len(str(value))) + str(value)

                if not check_palindrome(value):
                    continue
                tmp_re = n[0] + value + n[0]
                tmp_dis = abs(int(tmp_re) - int(n))
                # print(n,tmp_re,tmp_dis)
                if best_dis is None or tmp_dis < best_dis or (tmp_dis == best_dis and tmp_re < best_re):
                    best_re = tmp_re
                    best_dis = tmp_dis

            return best_re


class Solution2:
    def nearestPalindromic(self, n: str) -> str:
        n_int = int(n)
        if n_int < 110:
            return self.nearestPalindromic_simple(n_int)
        cand_list = []

        cand_list.append(cand1(n))  # 得到降位数的最近
        cand_list.append(cand2(n))  # 得到升位数的最近

        cand_list.append(cand3(n))  # 得到不升位数不降位数的最近

        min_dur = None
        min_re = None

        for cand_n in cand_list:
            if cand_n is None:
                continue
            dur_tmp = abs(int(cand_n) - n_int)
            if min_dur is None or dur_tmp < min_dur or (dur_tmp == min_dur and int(cand_n) < int(min_re)):
                min_re = cand_n
                min_dur = dur_tmp

        return min_re

    def nearestPalindromic_simple(self, n: int) -> str:
        if n == 0:
            return '1'
        i = 1
        while True:
            next_n = n - i
            if check_palindrome_int(next_n):
                return str(next_n)
            next_n = n + i
            if check_palindrome_int(next_n):
                return str(next_n)
            i += 1


class Solution:
    def find_larger(self, n):
        if len(n) == 0:
            return ''
        n_int = int(n)
        cand_list = []
        cand_list.append(self.increase(n))  # 得到升位数的最近

        if len(n) > 1:
            if check_palindrome(n[0:-1] + n[0]):
                cand_list.append(n[0:-1] + n[0])

            re = self.find_larger(n[1:-1])
            # print(n[1:-1],re)
            if not re is None:
                cand_list.append(n[0] + re + n[0])
            re = self.find_smaller(n[1:-1])
            if not re is None:
                cand_list.append(n[0] + re + n[0])

        min_dur = None
        min_re = None

        for cand_n in cand_list:
            if cand_n is None or cand_n <= n:
                continue
            dur_tmp = abs(int(cand_n) - n_int)
            if min_dur is None or dur_tmp < min_dur or (dur_tmp == min_dur and int(cand_n) < int(min_re)):
                min_re = cand_n
                min_dur = dur_tmp

        return min_re

    def increase(self, n):  # 得到升位数的最近
        if len(n) == 0 or n[0] == '9':
            return None
        n_len = len(n)
        first = str(int(n[0]) + 1)
        if n_len <= 1:
            return first
        else:
            return first + '0' * (n_len - 2) + first

    def decrease(self, n):  # 得到降位数的最近
        if len(n) == 0 or n[0] == '0':
            return None
        n_len = len(n)

        first = str(int(n[0]) - 1)
        if n_len <= 1:
            return first
        else:
            return first + '9' * (n_len - 2) + first

    def find_smaller(self, n):
        if len(n) == 0:
            return ''
        if n[0] == '-':
            return None

        n_int = int(n)
        cand_list = []
        cand_list.append(self.decrease(n))  # 得到降位数的最近

        if len(n) > 1:
            if check_palindrome(n[0:-1] + n[0]):
                cand_list.append(n[0:-1] + n[0])

            re = self.find_smaller(n[1:-1])
            if not re is None:
                cand_list.append(n[0] + re + n[0])

            re = self.find_larger(n[1:-1])
            if not re is None:
                cand_list.append(n[0] + re + n[0])

        # print(cand_list)

        min_dur = None
        min_re = None

        for cand_n in cand_list:
            if cand_n is None or cand_n >= n:
                continue
            dur_tmp = abs(int(cand_n) - n_int)
            if min_dur is None or dur_tmp < min_dur or (dur_tmp == min_dur and int(cand_n) < int(min_re)):
                min_re = cand_n
                min_dur = dur_tmp

        return min_re

    def nearestPalindromic(self, n: str) -> str:
        if n == '0':
            return '1'
        if n == '1':
            return '0'

        cand_list = []

        cand_list.append(self.find_larger(n))  # 得到更大的那个,不包含自身
        cand_list.append(self.find_smaller(n))  # 得到更小的那个,不包含自身
        if n[0] == '1':
            cand_list.append('9' * (len(n) - 1))
        if n[0] == '9':
            cand_list.append('1' + '0' * (len(n) - 1) + '1')

        min_dur = None
        min_re = None
        n_int = int(n)
        # print(cand_list)
        for cand_n in cand_list:
            if cand_n is None or cand_n[0] == '0':
                continue
            dur_tmp = abs(int(cand_n) - n_int)

            if min_dur is None or dur_tmp < min_dur or (dur_tmp == min_dur and int(cand_n) < int(min_re)):
                min_re = cand_n
                min_dur = dur_tmp

        return min_re


if __name__ == '__main__':

    solution1 = Solution2()  # 原始算法
    solution2 = Solution()  # 最新算法
    n = '107'
    # n= '10061'
    n1 = solution1.nearestPalindromic(n)
    n2 = solution2.nearestPalindromic(n)
    if n1 != n2:
        print(n, n1, n2)
        exit()
    for n in range(0, 100000):
        n = str(n)
        n1 = solution1.nearestPalindromic(n)
        n2 = solution2.nearestPalindromic(n)
        if n1 != n2:
            print(n, n1, n2)
            exit()
