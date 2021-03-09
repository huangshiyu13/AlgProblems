class Solution(object):
    def fizzBuzz(self, n):
        """
        :type n: int
        :rtype: List[str]
        """
        re = []
        for i in range(1,n+1):
            t = ''
            flag = False
            if i % 3 == 0:
                t = 'Fizz'
                flag = True

            if i % 5 == 0:
                t += 'Buzz'
                flag = True

            if not flag:
                t = str(i)

            re.append(t)
        return re

