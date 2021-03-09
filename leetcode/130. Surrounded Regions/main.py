class Solution(object):

    def solve(self, board):
        """
        :type board: List[List[str]]
        :rtype: void Do not return anything, modify board in-place instead.
        """

        self.board = board
        self.h = len(board)
        if self.h == 0:
            return
        self.w = len(board[0])
        if self.w == 0:
            return

        flag = []
        for _ in range(self.h):
            flag.append([0]*self.w)

        x = 0
        y = 0
        state = 'R'

        while True:
            if flag[x][y] == 0 and self.check(x,y):
                self.mark(x,y)
                flag[x][y] = 1

            if state == 'R':
                if y == self.w-1 or flag[x][y+1] == 1:
                    state = 'D'
                    x += 1
                    if x == self.h or flag[x][y] == 1:
                        break
                else:
                    y += 1
                continue

            if state == 'D':
                if x == self.h-1 or flag[x+1][y] == 1:
                    state = 'L'
                    y -= 1
                    if y == -1 or flag[x][y] == 1:
                        break
                else:
                    x += 1
                continue

            if state == 'L':
                if y == 0 or flag[x][y-1] == 1:
                    state = 'U'
                    x -= 1
                    if  x == -1 or flag[x][y] == 1:
                        break
                else:
                    y -= 1
                continue

            if state == 'U':
                if x == 0 or flag[x-1][y] == 1:
                    break
                else:
                    x -= 1
                continue

        # for b in board:
        #     print b
        # print ''

        for i in range(self.h):
            for j in range(self.w):
                if board[i][j] == 'S':
                    board[i][j] = 'O'
                else:
                    board[i][j] = 'X'


    def check(self,x,y):
        if not self.board[x][y] == 'O':
            return False
        if x*y == 0 or x == self.h-1 or y == self.w-1:
            return True
        ds = [[-1,0],[0,-1],[0,1],[1,0]]

        for d in ds:
            x_next, y_next = x+d[0], y+d[1]
            if self.board[x_next][y_next] == 'S':
                return True

        return False

    def mark(self,x,y):
        stack = []

        stack.append([x,y])

        while stack:
            p = stack.pop()
            self.board[p[0]][p[1]] = 'S'
            ds = [[-1,0],[0,-1],[0,1],[1,0]]
            for d in ds:
                x_next, y_next = p[0]+d[0], p[1]+d[1]
                # if x_next >=0 and y_next >=0 and x_next < self.h and y_next < self.w: print x,y, x_next,y_next
                if x_next >=0 and y_next >=0 and x_next < self.h and y_next < self.w and self.board[x_next][y_next] == 'O':
                    self.board[x_next][y_next] = 'S'
                    stack.append([x_next,y_next])

    # def escape(self, x , y):
    #     if x*y == 0 or x == self.h-1 or y == self.w-1:
    #         self.flag[x][y] = 2
    #         return True

    #     self.flag[x][y] = 1
    #     ds = [[-1,0],[0,-1],[0,1],[1,0]]
    #     for d in ds:
    #         x_next, y_next = x+d[0], y+d[1]

    #         if self.flag[x_next][y_next] == 2:
    #             self.flag[x][y] = 2
    #             return True

    #         if self.flag[x_next][y_next] == 1:
    #             continue

    #         if self.board[x_next][y_next] == 'O' and self.flag[x_next][y_next] == 0:
    #             self.flag[x_next][y_next] = 1
    #             if self.escape(x_next,y_next):
    #                 self.flag[x][y] = 2
    #                 return True


    #     self.board[x][y] = 'X'
    #     return False

s = Solution()
board = [
["O","O","O"],
["O","O","O"],
["O","O","O"]]
s.solve(board)

for b in board:
    print b

# for f in s.flag:
#     print f

