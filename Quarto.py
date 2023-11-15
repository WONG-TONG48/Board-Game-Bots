grid = ['    ' for _ in range(16)]
qualities = [('S','T'),('F','H'),('W','B'),('C','S')]
pieces= []

for i in qualities[0]:
    for j in qualities[1]:
        for l in qualities[2]:
            for k in qualities[3]:
                pieces.append(i+j+l+k)

def show_board():
    global grid
    print(f'{grid[0]}|{grid[1]}|{grid[2]}|{grid[3]}\n----|----|----|----\n{grid[4]}|{grid[5]}|{grid[6]}|{grid[7]}\n----|----|----|----\n{grid[8]}|{grid[9]}|{grid[10]}|{grid[11]}\n----|----|----|----\n{grid[12]}|{grid[13]}|{grid[14]}|{grid[15]}\n')

def get_move(player,piece):
    print(f'{player} turn, piece: {piece}')
    grid[int(input('Where would you like to play? '))] = piece
    return input('What piece do you want to give your oppnent? ')

def check_win(grid):
    for j in range(4):
        for i in range(4):
            if grid[i][j] == grid[i + 4][j] == grid[i+8][j] == grid[i+12][j] != ' ':
                return True
            elif grid[i*4][j] == grid[i*4+1][j] == grid[i*4+2][j] == grid[i*4+3][j] != ' ':
                return True
        if grid[0][j] == grid[5][j] == grid[10][j] == grid[15][j] != ' ':
            return True
        elif grid[3][j] == grid[6][j] == grid[9][j] == grid[12][j] != ' ':
            return True
    return False

def get_positions(grid,piece,pieces):
    positions = []
    for l,j in enumerate(grid):
        if j != '    ':
            continue
        new_grid = grid.copy()            
        new_grid[l] = piece
        for i in pieces:
            positions.append((new_grid,i))
    return positions

def evaluate(player,grid):
    if check_win(grid):
        if player == 'B':
            return 1
        else:
            return -1
    return 0

def minimax(grid,pieces,piece,depth,player,start,alpha=-2,beta=2):
    eval = evaluate(player,grid)
    if depth == 0 or eval != 0:
        return eval

    if player == 'O':
        max_eval = -2
        pos = None
        for i,j in get_positions(grid,piece,pieces):
            new_pieces = pieces.copy()
            new_pieces.remove(j)
            eval = minimax(i,new_pieces,j,depth-1,'B',False,alpha,beta)
            if start:
                if max_eval < eval:
                    pos = (i,j)
                    max_eval = eval
            else:
                max_eval = max(max_eval,eval)
            alpha = max(alpha,eval)
            if beta <= alpha or max_eval == 1:
                break
        if start:
            print(max_eval)
            return pos
        else:
            if max_eval == -2:
                return 0
            return max_eval

    if player == 'B':
        min_eval = 2
        pos = None
        for i,j in get_positions(grid,piece,pieces):
            new_pieces = pieces.copy()
            new_pieces.remove(j)
            eval = minimax(i,new_pieces,j,depth-1,'O',False,alpha,beta)
            if start:
                if min_eval > eval:
                    pos = (i, j)
                    min_eval = eval
            else:
                min_eval = min(min_eval,eval)
            beta = min(beta,eval)
            if beta <= alpha or min_eval == -1:
                break
        if start:
            print(min_eval)
            return pos
        else:
            if min_eval == 2:
                return 0
            return min_eval

piece = input('What piece do you want to give your oppnent? ')
pieces.remove(piece)
for i in range(17):
    show_board()
    if i % 2 == 0:
        grid, piece = minimax(grid,pieces,piece,6,'O',True)
        pieces.remove(piece)
    else:
     #   grid, piece = minimax(grid,pieces,piece,4,'B',True)
        #pieces.remove(piece)

        piece = get_move('B',piece)
        pieces.remove(piece)
    print(pieces)