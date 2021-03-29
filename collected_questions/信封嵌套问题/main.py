# https://leetcode-cn.com/problems/russian-doll-envelopes/solution/e-luo-si-tao-wa-xin-feng-wen-ti-by-leetc-wj68/

import bisect


class Solution:
    def maxEnvelopes(self, envelopes):
        if not envelopes:
            return 0

        n = len(envelopes)
        envelopes.sort(key=lambda x: (x[0], -x[1]))
        # print(envelopes)

        f = [envelopes[0][1]]
        envs = [envelopes[0]]
        for i in range(1, n):
            x2 = envelopes[i][1]

            if x2 > f[-1]:
                f.append(x2)
                envs.append(envelopes[i])
            else:
                index = bisect.bisect_left(f, x2)
                f[index] = x2
                envs[index] = envelopes[i]
            print(envelopes[i], envs)
        return len(f), envs


envelopes = [[3, 4], [2, 3], [4, 5], [1, 3], [2, 2], [3, 6], [1, 2], [3, 2], [2, 4]]

if __name__ == '__main__':
    solution = Solution()
    print(solution.maxEnvelopes(envelopes))
