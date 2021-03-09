class Solution(object):
    def fractionToDecimal(self, numerator, denominator):
        """
        :type numerator: int
        :type denominator: int
        :rtype: str
        """
        re = []
        sign = '' if numerator*denominator >= 0 else '-'

        re.append(sign)

        numerator, denominator = abs(numerator), abs(denominator)

        quotient, reminder = divmod(numerator, denominator)

        if reminder == 0:
            return re[0]+str(numerator/denominator)

        reminders = []
        reminders.append(reminder)
        re.append(str(quotient))
        re.append('.')

        while not reminder == 0:
            quotient, reminder = divmod(reminder*10, denominator)
            re.append(str(quotient))
            if reminder == 0:
                break
            if reminder in reminders:
                index = reminders.index(reminder)
                re.insert(index+3,'(')
                re.append(')')
                break
            reminders.append(reminder)
        return ''.join(re)

s = Solution()

print s.fractionToDecimal(1,-5)