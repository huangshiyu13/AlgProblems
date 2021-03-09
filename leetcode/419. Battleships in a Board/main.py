class Solution(object):
    def countBattleships(self, board):
        """
        :type board: List[List[str]]
        :rtype: int
        """
        i, j, re = 0, 0, 0
        h = len(board)
        w = len(board[0])
        for i in range(h):
            for j in range(w):
                if board[i][j] == 'X' and (i==0 or board[i-1][j] == '.') and (j==0 or board[i][j-1] == '.'):
                    re += 1

        return  re

s = Solution()
board = [['X','.','.','X'],['.','.','.','X'],['.','.','.','X']]
print s.countBattleships(board)

