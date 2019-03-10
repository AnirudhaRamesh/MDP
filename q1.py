from copy import deepcopy


class MDP : 
    """ Class MDP """
    def __init__(self, m, n, board, start_state, end_states, unit_step_reward, walls):
        self.m = m 
        self.n = n 
        self.board = board 
        self.old_board = deepcopy(board) 
        self.original_board = deepcopy(board)
        self.end_states = end_states 
        self.unit_step_reward = unit_step_reward
        self.start_state = start_state 
        self.walls = walls 
        self.init_walls()

    def print_board(self):
        for i in range(self.n):
            for j in range(self.m):
                if self.board[i][j]==None:
                    print(self.board[i][j], end = "\t")
                else:
                    print('%.3f'%self.board[i][j], end = "\t")
            print()

    def init_walls(self):
        for i in range(self.n):
            for j in range(self.m):
                if [i,j] in self.walls:
                    self.board[i][j] = None

    def VI(self):
        """ Function implementing Value Iteration """ 
        iteration_no = 0
        
        print(iteration_no," -----------")
        self.print_board()

        while True:
            iteration_no+=1
            max_change = 0 

            for i in range(n):
                for j in range(m):
                    if [i,j] not in self.walls and [i,j] not in self.end_states:
                        self.board[i][j] = self.update([i,j])
                        if self.old_board[i][j]!=0:
                            temp = abs((self.board[i][j] - self.old_board[i][j])/self.old_board[i][j])
                        else: 
                            temp = 100.0
                        max_change = max(temp,max_change)
                        

            print("\n",iteration_no," -----------")
            self.print_board()

            self.old_board = deepcopy(self.board)

            if max_change <= 0.01:
                break

        print("\nFinal Policy\n")
        self.print_policy()        
        
    def update(self,coords):
        x,y = coords

        utility_north = self.get_util(self.old_board[x][y], x, y-1) 
        utility_south = self.get_util(self.old_board[x][y], x, y+1) 
        utility_west = self.get_util(self.old_board[x][y], x-1, y) 
        utility_east = self.get_util(self.old_board[x][y], x+1, y) 

        value_north = 0.8 * utility_north + 0.1 * utility_east + 0.1 * utility_west
        value_south = 0.8 * utility_south + 0.1 * utility_east + 0.1 * utility_west
        value_east = 0.8 * utility_east + 0.1 * utility_north + 0.1 * utility_south
        value_west = 0.8 * utility_west + 0.1 * utility_north + 0.1 * utility_south

        new_value = self.unit_step_reward + 0.99*max(value_north, value_east, value_south, value_west) + self.original_board[x][y]

        return new_value

    def get_util(self, value, x,y):
        if x < 0 or y < 0 or x >= self.n or y >= self.m or self.old_board[x][y] == None :
            return value  
        return self.old_board[x][y]


    def print_policy(self):
        for i in range(self.n):
            for j in range(self.m):
                if [i,j] not in walls and [i,j] not in end_states:
                    direction = self.get_dir(i,j)
                    print(direction, end=" ")
                else: 
                    print("-", end = " ")
            print()

    def get_dir(self,x,y):
        # if x-1 < 0 or y < 0 or x-1 >= self.n or y >= self.m or self.board[x-1][y] == None:
        #     north = -100000
        # else :
        #     north = self.board[x-1][y]*0.8
        #     if self.board[x][y-1] != None:
        #         north += self.board[x][y-1]*0.1
        #     if self.board[x][y+1] != None:
        #         north += self.board[x][y+1]*0.1


        # if x+1 < 0 or y < 0 or x+1 >= self.n or y >= self.m or self.board[x+1][y] == None :
        #     south = -100000
        # else :
        #     south = self.board[x+1][y]*0.8 + self.board[x][y-1]*0.1 +  self.board[x][y+1]*0.1

        # if x < 0 or y-1 < 0 or x >= self.n or y-1 >= self.m or self.board[x][y-1] == None:
        #     west = -100000
        # else :
        #     west = self.board[x][y-1]

        # if x < 0 or y+1 < 0 or x >= self.n or y+1 >= self.m or self.board[x][y+1] == None:
        #     east = -100000
        # else :
        #     east = self.board[x][y+1]

        utility_north = self.get_util(self.old_board[x][y], x-1, y) 
        utility_south = self.get_util(self.old_board[x][y], x+1, y)
        utility_west = self.get_util(self.old_board[x][y], x, y-1) 
        utility_east = self.get_util(self.old_board[x][y], x, y+1)

        north = utility_north * 0.8 + utility_east*0.1 + utility_west*0.1
        south = utility_south * 0.8 + utility_east*0.1 + utility_west*0.1
        east = utility_east * 0.8 + utility_south * 0.1 + utility_north *0.1 
        west = utility_west * 0.8 + utility_north * 0.1 + utility_south * 0.1 
        
        max_dir = max(north, east, south, west)

        if max_dir == north:
            return 'N'
        if max_dir == south:
            return 'S'
        if max_dir == east:
            return 'E'
        if max_dir == west:
            return 'W'

        return '-' 




            


n,m = input().split()
n = int(n) 
m = int(m)

board = [[ 0 for i in range(m)]for j in range(n)]

for i in range(n):
    temp = input().split()
    for j in range(m):
        board[i][j] = float(temp[j]) 

e,w = input().split()
e = int(e)
w = int(w)

end_states = [ [0,0] for i in range(e)]
walls = [ [0,0] for i in range(w)]

for i in range(e):
    temp = input().split()
    end_states[i][0] = int(temp[0])
    end_states[i][1] = int(temp[1])

for i in range(w):
    temp = input().split()
    walls[i][0] = int(temp[0])
    walls[i][1] = int(temp[1])

start_state = input().split()
start_state[0] = int(start_state[0])
start_state[1] = int(start_state[1])

unit_reward = input()
unit_reward = float(unit_reward)

a = MDP(m,n,board,start_state,end_states,unit_reward,walls)

a.VI()





