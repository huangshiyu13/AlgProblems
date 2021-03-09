class Solution:
    def plusOne_my(self, digits):
        re = []
        before = 0
        first= True
        for digit in digits[::-1]:
            if first:
                digit+=1+before
                first = False
            else:
                digit+=before
            
            before = int(digit/10)
            digit%=10
            re.append(digit)
        if before == 1:
            re.append(before)
        re.reverse()
        return re
        
    def plusOne_2(self,digits):
        for i in range(len(digits))[::-1]:
            d = digits[i]+1
            if d < 10:
                digits[i] = d
                return digits
            else:
                digits[i] = int(d%10)
        return [1]+digits

    def plusOne(self,digits):
        return [int(_) for _ in str( int(''.join([str(_) for _ in digits]))+1 )]

digits = [9,9]
s = Solution()
print(s.plusOne(digits))

        