grid_x = 7
grid_y = 6
grid = [' ' for _ in range(grid_x * grid_y)]

def show_board():
    global grid
    for i in range(grid_y):
        string = '|'
        for j in range(grid_x):
            if grid[i * grid_x + j] == ' ':
                string += str(i * grid_x + j)
                if i * grid_x + j < 10:
                    string += ' '
            else:
                string = string + grid[i * grid_x + j] + ' '
            string += '|'
        print(string)

def get_move(player):
    print(f'{player} turn:')
    grid[int(input('Where would you like to play? '))] = player

def check_win(grid):
    for i in range(grid_x):
        temp = 0
        prev = None
        for j in range(grid_y):
            cur = grid[j * grid_x + i]
            if cur == prev:
                temp += 1
            else:
                prev = cur
                temp = 1
            if temp >= 4 and cur != ' ':
                return True
    for j in range(grid_y):
        temp = 0
        prev = None
        for i in range(grid_x):
            cur = grid[j * grid_x + i]
            if cur == prev:
                temp += 1
            else:
                prev = cur
                temp = 1
            if temp >= 4 and cur != ' ':
                return True
    for i in [3]:
        for j in range(grid_y):
            cur = grid[j * grid_x + i]
            if cur == ' ': continue
            ind = j * grid_x + i
            temp = 0
            while grid[ind] == cur:
                temp += 1
                ind += grid_x + 1
                if ind > len(grid) - 1:
                    break
            ind = j * grid_x + i
            temp -= 1
            while grid[ind] == cur:
                temp += 1
                ind -= (grid_x + 1)
                if ind < 0:
                    break
            if temp >= 4:
                return True
            ind = j * grid_x + i
            temp = 0
            while grid[ind] == cur:
                temp += 1
                ind += grid_x - 1
                if ind > len(grid) - 1:
                    break
            ind = j * grid_x + i
            temp -= 1
            while grid[ind] == cur:
                temp += 1
                ind -= (grid_x - 1)
                if ind < 0:
                    break
            if temp >= 4:
                return True

    return False

def get_positions(grid,player):
    positions = []
    for i in [3,4,2,1,5,6,0]:
        ind = i
        while grid[ind] == ' ':
            ind += grid_x
            if ind > len(grid) - 1:
                break
        ind -= grid_x
        if ind < 0:
            continue
        new_grid = grid.copy()
        new_grid[ind] = player
        positions.append(new_grid)
    return positions

def evaluate(player,grid):
    if check_win(grid):
        if player == 'B':
            return 1
        else:
            return -1
    return 0

def minimax(grid,depth,player,start,alpha=-99,beta=99):
    eval = evaluate(player,grid)
    if depth == 0 or eval != 0:
        return eval * (depth + 1)

    if player == 'O':
        max_eval = -999
        pos = None
        for i in get_positions(grid,player):
            eval = minimax(i,depth-1,'B',False,alpha,beta)
            if start:
                if max_eval < eval:
                    pos = i
                    max_eval = eval
            else:
                max_eval = max(max_eval,eval)
            alpha = max(alpha,eval)
            if beta <= alpha:
                break
        if start:
            print(max_eval)
            return pos
        else:
            return max_eval

    if player == 'B':
        min_eval = 999
        pos = None
        for i in get_positions(grid,player):
            eval = minimax(i,depth-1,'O',False,alpha,beta)
            if start:
                if min_eval > eval:
                    pos = i
                    min_eval = eval
            else:
                min_eval = min(min_eval,eval)
            beta = min(beta,eval)
            if beta <= alpha:
                break
        if start:
            print(min_eval)
            return pos
        else:
            return min_eval

for i in range(42):
    show_board()
    if i % 2 == 1:
        grid = minimax(grid,9,'O',True)
    else:
        get_move('B')