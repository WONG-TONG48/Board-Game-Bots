import pygame as pg
from os.path import join
import chess

WIDTH, HEIGHT = 720, 720

window = pg.display.set_mode((WIDTH,HEIGHT))

transposition_table = {}

piece_squre_values = {chess.PAWN:([ 0,  0,  0,  0,  0,  0,  0,  0,
                                    50, 50, 50, 50, 50, 50, 50, 50,
                                    10, 10, 20, 30, 30, 20, 10, 10,
                                    5,  5, 10, 25, 25, 10,  5,  5,
                                    0,  0,  0, 20, 20,  0,  0,  0,
                                    5, -5,-10,  0,  0,-10, -5,  5,
                                    5, 10, 10,-20,-20, 10, 10,  5,
                                    0,  0,  0,  0,  0,  0,  0,  0],
                                    [ 0,  0,  0,  0,  0,  0,  0,  0,
                                    50, 50, 50, 50, 50, 50, 50, 50,
                                    40, 40, 40, 40, 40, 40, 40, 40,
                                    30,  30, 30, 30, 30, 30,  30,  30,
                                    20, 20,20, 20,  20,20, 20,  20,
                                    10, 10, 10,10,10, 10, 10,  10,
                                    0,  0,  0,  0,  0,  0,  0,  0,
                                    0,  0,  0,  0,  0,  0,  0,  0]),
                      chess.KNIGHT:([-50,-40,-30,-30,-30,-30,-40,-50,
                                    -40,-20,  0,  0,  0,  0,-20,-40,
                                    -30,  0, 10, 15, 15, 10,  0,-30,
                                    -30,  5, 15, 20, 20, 15,  5,-30,
                                    -30,  0, 15, 20, 20, 15,  0,-30,
                                    -30,  5, 10, 15, 15, 10,  5,-30,
                                    -40,-20,  0,  5,  5,  0,-20,-40,
                                    -50,-40,-30,-30,-30,-30,-40,-50],
                                    [-50,-40,-30,-30,-30,-30,-40,-50,
                                    -40,-20,  0,  0,  0,  0,-20,-40,
                                    -30,  0, 10, 15, 15, 10,  0,-30,
                                    -30,  5, 15, 20, 20, 15,  5,-30,
                                    -30,  0, 15, 20, 20, 15,  0,-30,
                                    -30,  5, 10, 15, 15, 10,  5,-30,
                                    -40,-20,  0,  5,  5,  0,-20,-40,
                                    -50,-40,-30,-30,-30,-30,-40,-50],),
                      chess.BISHOP:([-20,-10,-10,-10,-10,-10,-10,-20,
                                    -10,  0,  0,  0,  0,  0,  0,-10,
                                    -10,  0,  5, 10, 10,  5,  0,-10,
                                    -10,  5,  5, 10, 10,  5,  5,-10,
                                    -10,  0, 10, 10, 10, 10,  0,-10,
                                    -10, 10, 10, 10, 10, 10, 10,-10,
                                    -10,  5,  0,  0,  0,  0,  5,-10,
                                    -20,-10,-10,-10,-10,-10,-10,-20],
                                    [-20,-10,-10,-10,-10,-10,-10,-20,
                                    -10,  0,  0,  0,  0,  0,  0,-10,
                                    -10,  0,  5, 10, 10,  5,  0,-10,
                                    -10,  5,  5, 10, 10,  5,  5,-10,
                                    -10,  0, 10, 10, 10, 10,  0,-10,
                                    -10, 10, 10, 10, 10, 10, 10,-10,
                                    -10,  5,  0,  0,  0,  0,  5,-10,
                                    -20,-10,-10,-10,-10,-10,-10,-20]),
                      chess.ROOK:([ 0,  0,  0,  0,  0,  0,  0,  0,
                                    5, 10, 10, 10, 10, 10, 10,  5,
                                    -5,  0,  0,  0,  0,  0,  0, -5,
                                    -5,  0,  0,  0,  0,  0,  0, -5,
                                    -5,  0,  0,  0,  0,  0,  0, -5,
                                    -5,  0,  0,  0,  0,  0,  0, -5,
                                    -5,  0,  0,  0,  0,  0,  0, -5,
                                    0,  0,  0,  5,  5,  0,  0,  0],
                                    [ 0,  0,  0,  0,  0,  0,  0,  0,
                                    5, 10, 10, 10, 10, 10, 10,  5,
                                    -5,  0,  0,  0,  0,  0,  0, -5,
                                    -5,  0,  0,  0,  0,  0,  0, -5,
                                    -5,  0,  0,  0,  0,  0,  0, -5,
                                    -5,  0,  0,  0,  0,  0,  0, -5,
                                    -5,  0,  0,  0,  0,  0,  0, -5,
                                    0,  0,  0,  5,  5,  0,  0,  0]),
                      chess.QUEEN:([-20,-10,-10, -5, -5,-10,-10,-20,
                                    -10,  0,  0,  0,  0,  0,  0,-10,
                                    -10,  0,  5,  5,  5,  5,  0,-10,
                                    -5,  0,  5,  5,  5,  5,  0, -5,
                                    0,  0,  5,  5,  5,  5,  0, -5,
                                    -10,  5,  5,  5,  5,  5,  0,-10,
                                    -10,  0,  5,  0,  0,  0,  0,-10,
                                    -20,-10,-10, -5, -5,-10,-10,-20],
                                    [-20,-10,-10, -5, -5,-10,-10,-20,
                                    -10,  0,  0,  0,  0,  0,  0,-10,
                                    -10,  0,  5,  5,  5,  5,  0,-10,
                                    -5,  0,  5,  5,  5,  5,  0, -5,
                                    0,  0,  5,  5,  5,  5,  0, -5,
                                    -10,  5,  5,  5,  5,  5,  0,-10,
                                    -10,  0,  5,  0,  0,  0,  0,-10,
                                    -20,-10,-10, -5, -5,-10,-10,-20]),
                      chess.KING:([-30,-40,-40,-50,-50,-40,-40,-30,
                                -30,-40,-40,-50,-50,-40,-40,-30,
                                -30,-40,-40,-50,-50,-40,-40,-30,
                                -30,-40,-40,-50,-50,-40,-40,-30,
                                -20,-30,-30,-40,-40,-30,-30,-20,
                                -10,-20,-20,-20,-20,-20,-20,-10,
                                20, 20,  0,  0,  0,  0, 20, 20,
                                20, 30, 10,  0,  0, 10, 30, 20],
                                [-30,-20,-10,  0,  0,-10,-20,-30,
                                -30,-10, 20, 30, 30, 20,-10,-30,
                                -30,-10, 30, 40, 40, 30,-10,-30,
                                -30,-10, 30, 40, 40, 30,-10,-30,
                                -30,-10, 20, 30, 30, 20,-10,-30,
                                -30,-30,  0,  0,  0,  0,-30,-30,
                                -50,-30,-30,-30,-30,-30,-30,-50])}

piece_values = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 0 # Ignore the king value
}

def material_score(board):
    material_score = 0
    end_game = 0 if len(board.piece_map()) > 13 else 1
    # Loop over the piece map
    for square,piece in board.piece_map().items():
        # Add or subtract the piece value according to the color
        if piece.color == chess.WHITE:
            material_score += piece_values[piece.piece_type] + list(reversed(piece_squre_values[piece.piece_type][end_game]))[square]
        else:
            material_score -= piece_values[piece.piece_type] + piece_squre_values[piece.piece_type][end_game][square]

    return material_score

def is_movement(board,piece_ind,mouse_ind):
    for i in board.legal_moves:
        if i.from_square == piece_ind and i.to_square == mouse_ind:
            return True
    return False

class Board(chess.Board):
    #stores all of the sprites into a dictionry that sorts by color and then piece type
    tile_len = 90
    tile_cols = ((255,255,255),(0,100,255))
    x_offset = (WIDTH - tile_len * 8) // 2
    y_offset = (HEIGHT - tile_len * 8) // 2
    radius = (tile_len / 2 - 10)
    circle = pg.Surface((radius*2, radius*2), pg.SRCALPHA)
    pg.draw.circle(circle,(150,150,150,150),(radius,radius),radius)
    sprites = {True:{
                    6:pg.transform.scale_by(pg.image.load(join('Board Game Bots','Chess pieces','tile007.png')),tile_len / 60).convert_alpha(),
                    5:pg.transform.scale_by(pg.image.load(join('Board Game Bots','Chess pieces','tile006.png')),tile_len / 60).convert_alpha(),
                    4:pg.transform.scale_by(pg.image.load(join('Board Game Bots','Chess pieces','tile008.png')),tile_len / 60).convert_alpha(),
                    2:pg.transform.scale_by(pg.image.load(join('Board Game Bots','Chess pieces','tile009.png')),tile_len / 60).convert_alpha(),
                    3:pg.transform.scale_by(pg.image.load(join('Board Game Bots','Chess pieces','tile010.png')),tile_len / 60).convert_alpha(),
                    1:pg.transform.scale_by(pg.image.load(join('Board Game Bots','Chess pieces','tile011.png')),tile_len / 60).convert_alpha()},
                False:{
                    6:pg.transform.scale_by(pg.image.load(join('Board Game Bots','Chess pieces','tile001.png')),tile_len / 60).convert_alpha(),
                    5:pg.transform.scale_by(pg.image.load(join('Board Game Bots','Chess pieces','tile000.png')),tile_len / 60).convert_alpha(),
                    4:pg.transform.scale_by(pg.image.load(join('Board Game Bots','Chess pieces','tile002.png')),tile_len / 60).convert_alpha(),
                    2:pg.transform.scale_by(pg.image.load(join('Board Game Bots','Chess pieces','tile003.png')),tile_len / 60).convert_alpha(),
                    3:pg.transform.scale_by(pg.image.load(join('Board Game Bots','Chess pieces','tile004.png')),tile_len / 60).convert_alpha(),
                    1:pg.transform.scale_by(pg.image.load(join('Board Game Bots','Chess pieces','tile005.png')),tile_len / 60).convert_alpha()}
                }
    
    def get_pos_positions(self):
        for move in self.legal_moves:
            new_board = self.copy()
            new_board.push(move)
            yield new_board
    
    def draw(self,selected):

        for i in range(8):
            for j in range(8):
                pg.draw.rect(window,self.tile_cols[(i + j) % 2],(i * self.tile_len + self.x_offset,j * self.tile_len + self.y_offset,self.tile_len,self.tile_len))

        def draw_circle(index):
            col = 7 - index // 8
            row = index % 8
            window.blit(self.circle,(row * self.tile_len + self.x_offset + (self.tile_len - self.radius * 2) / 2,col * self.tile_len + self.y_offset + (self.tile_len - self.radius * 2) / 2))

        def draw_piece(color,piece,index):
            col = 7 - index // 8
            row = index % 8
            window.blit(self.sprites[color][piece],(row * self.tile_len + self.x_offset,col * self.tile_len + self.y_offset))

        for i,j in self.piece_map().items():
            draw_piece(j.color,j.piece_type,i)

        if selected is None:
            return
        
        for i in self.legal_moves:
            if i.from_square == selected:
                draw_circle(i.to_square)

def evaluate(board):
    if board.is_stalemate() or board.is_insufficient_material() or board.is_fivefold_repetition() or board.is_repetition() or board.can_claim_threefold_repetition():        
        return 0
    if board.is_checkmate():
        if board.turn == chess.WHITE:
            return -99999
        else:
            return 99999
    return material_score(board)


def minimax(board,depth,alpha = -99999999,beta=99999999,start =False):
    if depth == 0 or board.outcome() != None or board.can_claim_threefold_repetition():
        return evaluate(board)
    
    fen = board.fen()

    if not start:
        val = transposition_table.get(fen)
        if val != None and val[1] >= depth:
            return val[0]
        
    if len(transposition_table) > 5000:
        transposition_table.pop(next(iter(transposition_table)))
    
    if board.turn:
        max_eval = -99999999
        for i in board.get_pos_positions():
            eval = minimax(i,depth-1,alpha,beta)
            if max_eval < eval:
                pos = i
            max_eval = max(max_eval,eval)
            alpha = max(alpha,eval)
            if beta <= alpha:
                break
        transposition_table[fen] = (max_eval,depth)
        if start:
            print(max_eval)
            return pos
        return max_eval
    else:
        min_eval = 99999999
        pos = None
        for i in board.get_pos_positions():
            eval = minimax(i,depth-1,alpha,beta)
            if min_eval > eval:
                pos = i
            min_eval = min(min_eval,eval)
            beta = min(beta,eval)
            if beta <= alpha:
                break
        transposition_table[fen] = (min_eval,depth)
        if start:
            print(min_eval)
            return pos
        return min_eval


def draw(board,selected):
    window.fill((0,0,0))

    board.draw(selected)

    pg.display.update()

def main():
    global transposition_table
    board = Board()
    board = minimax(board,4,start=True)
    draw(board,None)
    run = True
    selected = None
    while run:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                break
            elif event.type == pg.MOUSEBUTTONDOWN:
                info = event.dict
                col = (info['pos'][0] - Board.x_offset) // Board.tile_len
                row = 7 - (info['pos'][1] - Board.y_offset) // Board.tile_len
                index = row * 8 + col
                if selected is None or not is_movement(board,selected,index):
                    selected = index
                    
                else:
                    move = chess.Move(selected,index)
                    board.push(move)
                    white_pawns = board.pieces(chess.PAWN, chess.WHITE)
                    black_pawns = board.pieces(chess.PAWN, chess.BLACK)
                    for i in white_pawns:
                        if i > 54:
                            board.set_piece_at(i, chess.Piece(chess.QUEEN, chess.WHITE), promoted=True)
                    for i in black_pawns:
                        if i < 8:
                            board.set_piece_at(i, chess.Piece(chess.QUEEN, chess.BLACK), promoted=True)
                    selected = None
                    draw(board,None)
                    board = minimax(board,4,start=True)
                


        draw(board,selected)

    pg.quit()
    quit()

if __name__ == '__main__':
    main()