states = ['space', 'word']


class Solution:
    def reverseWords(self, s: str) -> str:
        s = [ss.strip() for ss in s.split(' ')]
        re = ''
        for ss in s[::-1]:
            re += ss
            if not ss == '':
                re += ' '
        return re[:-1]


if __name__ == '__main__':
    s = "  hello world  "
    solution = Solution()
    print(solution.reverseWords(s))
