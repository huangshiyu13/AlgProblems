class Solution(object):
    def calPoints(self, ops):
        """
        :type ops: List[str]
        :rtype: int
        """

        record = []
        sum = 0
        for op in ops:
            if op == 'C':
                if record:
                    a = record.pop()
                    sum -= a
                continue
            if op == 'D':
                if record:
                    a = 2*record[-1]
                    sum += a
                    record.append(a)
                continue
            if op == '+':
                if len(record) >= 2:
                    a = record[-1]+record[-2]
                else:
                    if len(record) == 1:
                        a = record[0]
                    else:
                        a = 0
                sum += a
                record.append(a)

                continue
            a = int(op)
            record.append(a)
            sum += a
        return sum


