import copy
import pygame as pg

grid = [['  '] for _ in range(9)]
sizes = ['s','m','l']
size_vals = {'s':0,'m':1,'l':2}
pieces={'O':{'s':2,'m':2,'l':2},'B':{'s':2,'m':2,'l':2}}
WIN_SIZE = 600
window = pg.display.set_mode((WIN_SIZE,WIN_SIZE))
pg.display.set_caption('Gobblet Gobblers')

def show_board():
    global grid, o_p, b_p
    print(f'{grid[0][-1]}|{grid[1][-1]}|{grid[2][-1]}\n--|--|--\n{grid[3][-1]}|{grid[4][-1]}|{grid[5][-1]}\n--|--|--\n{grid[6][-1]}|{grid[7][-1]}|{grid[8][-1]}\n')

def check_win(player,grid):
    for i in range(3):
        if grid[i][-1][0] == grid[i + 3][-1][0] == grid[i+6][-1][0] == player:
            return True
        elif grid[i*3][-1][0] == grid[i*3+1][-1][0] == grid[i*3+2][-1][0] == player:
            return True
    if grid[0][-1][0] == grid[4][-1][0] == grid[8][-1][0] == player:
        return True
    elif grid[2][-1][0] == grid[4][-1][0] == grid[6][-1][0] == player:
        return True
    return False

def get_positions(grid,player,pieces):
    positions = []
    for i in sizes:
        if pieces[i] < 1:
            continue
        for l,j in enumerate(grid):
            j = j[-1]
            new_grid = copy.deepcopy(grid)
            if j == '  ':
                new_grid[l].append(player + i)
                positions.append((new_grid,i))
                continue
            elif size_vals[i] > size_vals[j[1]]:
                new_grid[l].append(player + i)
                positions.append((new_grid,i))
                continue
    for k,i in enumerate(grid):
        if i[-1][0] != player or i == ['  ']:
            continue
        i = i.copy()
        for l,j in enumerate(grid):
            new_grid = copy.deepcopy(grid)
            j = j[-1]
            if j == '  ':
                new_grid[l].append(new_grid[k].pop(-1))
                positions.append((new_grid,None))
                continue
            elif size_vals[i[-1][1]] > size_vals[j[1]]:
                new_grid[l].append(new_grid[k].pop(-1))
                positions.append((new_grid,None))
                continue
    return positions

def evaluate(grid):
    if check_win('O',grid):
        return 1
    elif check_win('B',grid):
        return -1
    return 0

def minimax(grid,o_pieces,b_pieces,depth,player,start,alpha=-2,beta=2):
    eval = evaluate(grid)
    if depth == 0 or eval != 0:
        return eval

    if player == 'O':
        max_eval = -2
        pos = None
        for i,j in get_positions(grid,'O',o_pieces):
            new_o_pieces = o_pieces.copy()
            if j:
                new_o_pieces[j] -= 1
            eval = minimax(i,new_o_pieces,b_pieces,depth-1,'B',False,alpha,beta)
            if start:
                if max_eval < eval:
                    pos = i
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
        for i,j in get_positions(grid,'B',b_pieces):
            new_b_pieces = b_pieces.copy()
            if j:
                new_b_pieces[j] -= 1
            eval = minimax(i,o_pieces,new_b_pieces,depth-1,'O',False,alpha,beta)
            if start:
                if min_eval > eval:
                    pos = i
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

for i in range(99):
    show_board()
    if i % 2 == 0:
        grid = minimax(grid,pieces['O'],pieces['B'],6,'O',True)
        old_pieces = {'s':2,'m':2,'l':2}
        for i in grid:
            for j in i:
                if j[0] != 'O':
                    continue
                old_pieces[j[1]] -= 1
        pieces['O'] = old_pieces
    else:

        get_move('B')
    print(pieces)