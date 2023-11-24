import copy
import pygame as pg
pg.font.init()

grid = [['  '] for _ in range(9)]
sizes = ['s','m','l']
size_vals = {'s':0,'m':1,'l':2}
pieces={'O':{'s':2,'m':2,'l':2},'B':{'s':2,'m':2,'l':2}}
pos_to_str = {0:'Top left',1:'Top middle',2:'Top right',3:'Middle left',4:'Center',5:'Middle right',6:'Bottom left',7:'Bottom Middle',8:'Bottom Right'}
size_to_str = {'s':'Small','m':'Medium','l':'Large'}
WIN_SIZE = 700
font = pg.font.SysFont('comicsans',30)
pos_grid = [(175, 174),(340, 174),(494, 184),(157, 351),(340, 347),(522, 345),(164, 524),(351, 518),(535, 520)]
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
        if i[-1][0] != player:
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

def stacked_pieces(player,grid):
    ans = 0
    for i in grid:
        if i == ['  ']:
            continue
        if i[-1][0] == i[-2][0] == player:
            ans += 1
    return ans

def evaluate(grid):
    ans = 0
    if check_win('O',grid):
        ans += 2
    elif check_win('B',grid):
        ans += -2
    ans += (stacked_pieces('O',grid) - stacked_pieces('B',grid)) / 20
    return ans

def minimax(grid,o_pieces,b_pieces,depth,player,start,alpha=-999,beta=999):
    eval = evaluate(grid)
    if depth == 0 or abs(eval) >  1:
        return eval * (depth +1)

    if player == 'O':
        max_eval = -999
        pos = None
        for i,j in get_positions(grid,'O',o_pieces):
            new_o_pieces = o_pieces.copy()
            if j:
                new_o_pieces[j] -= 1
            eval = minimax(i,new_o_pieces,b_pieces,depth-1,'B',False,alpha,beta)
            if start:
                if max_eval < eval:
                    pos = (i,j)
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
            if beta <= alpha:
                break
        if start:
            print(min_eval)
            return pos
        else:
            return min_eval
        

class Piece:
    pieces = []

    def __init__(self,type,size,radius,color,pos):
        self.pieces.append(self)
        self.type = type
        self.radius = radius
        self.pos = pos
        self.size = size
        self.color = color
        self.selected = False
        self.ind = None

    def __lt__(self,other):
        return self.size < other.size

    def draw(self):
        if self.selected:
            pg.draw.circle(window,'purple',self.pos,self.radius)
        else:
            pg.draw.circle(window,self.color,self.pos,self.radius)
        
def draw_grid():
    rect1 = pg.Rect(100,60,WIN_SIZE - 200,25)
    rect2 = pg.Rect(60,100,25,WIN_SIZE - 200)
    for _ in range(2):
        rect2.x += WIN_SIZE // 3 - 50
        pg.draw.rect(window,'black',rect2)

    for _ in range(2):
        rect1.y += WIN_SIZE // 3 - 50
        pg.draw.rect(window,'black',rect1)

def draw(best_move):
    window.fill('white')

    draw_grid()

    for i in Piece.pieces:
        i.draw()

    window.blit(font.render(f'Best Move: {best_move}',1,(0,0,0)),(0,50))

    pg.display.update()

def dist(cord1,cord2):
    return (abs(cord1[0] - cord2[0]) + abs(cord1[1] - cord2[1])) ** 0.5

def get_closest_position():
    closest = [None,999999]
    mouse = pg.mouse.get_pos()
    for j,i in enumerate(pos_grid):
        distance = dist(i,mouse)
        if distance < closest[1]:
            closest[1] = distance
            closest[0] = (j,i)
    return closest[0]

def get_closest_circle():
    closest = [None,999999]
    mouse = pg.mouse.get_pos()
    for i in reversed(Piece.pieces):
        distance = dist(i.pos,mouse)
        if distance < closest[1]:
            closest[1] = distance
            closest[0] = i
    return closest[0]

def get_dif(old_grid,piece):
    ans = ''
    if piece:
        ans += piece
        for i,j in enumerate(zip(old_grid,grid)):
            if j[0] != j[1]:
                ans += str(i)
                return f'{size_to_str[ans[0]]} to {pos_to_str[int(ans[-1])]}'
    else:
        ans = ['','']
        for i,j in enumerate(zip(old_grid,grid)):
            if len(j[0]) != len(j[1]):
                if len(j[0]) > len(j[1]):
                    ans[1] = j[0][-1] + str(i)
                elif len(j[0]) < len(j[1]):
                    ans[0] = j[1][-1] + str(i)
        return f'{pos_to_str[int(ans[0][-1])]} to {pos_to_str[int(ans[1][-1])]}'

def main():
    for i in range(2):
        y = i * (WIN_SIZE - 80) + 40
        piece = 'O'
        color = 'orange'
        if i == 1:
            piece = 'B'
            color = 'blue'
        for l,k,j in zip(range(6),[10,10,20,20,40,40],['s','s','m','m','l','l']):
            Piece(piece,j,k,color,(l * 80 + 200,y))
    Piece.pieces.sort(reverse=True)
    run = True
    selected = None
    best_move = 'Small to Top left'
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                break
            elif event.type == pg.MOUSEBUTTONDOWN:
                if selected is None:
                    selected = get_closest_circle()
                    selected.selected = True
                else:
                    ind,pos = get_closest_position()
                    if selected.ind != None:
                        grid[selected.ind].pop(-1)
                    else:
                        pieces[selected.type][selected.size] -= 1
                    selected.ind = ind
                    selected.pos = pos
                    grid[ind].append(selected.type + selected.size)
                    if selected.type == 'B':
                        best_move = get_dif(*minimax(grid,pieces['O'],pieces['B'],5,'O',True))
                    selected.selected = False
                    selected = None
                    print(evaluate(grid))

        draw(best_move)

    pg.quit()
    quit()

if __name__ == '__main__':
    main()