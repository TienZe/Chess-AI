"""
Handling the AI moves.
Có sử dụng thuật toán Negamax và cắt tỉa Alpha-beta
"""
import random

piece_score = {"K": 0, "Q": 9, "R": 5, "B": 3, "N": 3, "p": 1}
#Đánh giá mức độ quan trọng của từng quân cờ (VD: 0 là không thể để mất,Q là quan trọng nhất và chỉ mang tính tương đối)

knight_scores = [[0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0],
                 [0.1, 0.3, 0.5, 0.5, 0.5, 0.5, 0.3, 0.1],
                 [0.2, 0.5, 0.6, 0.65, 0.65, 0.6, 0.5, 0.2],
                 [0.2, 0.55, 0.65, 0.7, 0.7, 0.65, 0.55, 0.2],
                 [0.2, 0.5, 0.65, 0.7, 0.7, 0.65, 0.5, 0.2],
                 [0.2, 0.55, 0.6, 0.65, 0.65, 0.6, 0.55, 0.2],
                 [0.1, 0.3, 0.5, 0.55, 0.55, 0.5, 0.3, 0.1],
                 [0.0, 0.1, 0.2, 0.2, 0.2, 0.2, 0.1, 0.0]]

bishop_scores = [[0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0],
                 [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                 [0.2, 0.4, 0.5, 0.6, 0.6, 0.5, 0.4, 0.2],
                 [0.2, 0.5, 0.5, 0.6, 0.6, 0.5, 0.5, 0.2],
                 [0.2, 0.4, 0.6, 0.6, 0.6, 0.6, 0.4, 0.2],
                 [0.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.2],
                 [0.2, 0.5, 0.4, 0.4, 0.4, 0.4, 0.5, 0.2],
                 [0.0, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.0]]

rook_scores = [[0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25],
               [0.5, 0.75, 0.75, 0.75, 0.75, 0.75, 0.75, 0.5],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.0, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.0],
               [0.25, 0.25, 0.25, 0.5, 0.5, 0.25, 0.25, 0.25]]

queen_scores = [[0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0],
                [0.2, 0.4, 0.4, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.3, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.4, 0.4, 0.5, 0.5, 0.5, 0.5, 0.4, 0.3],
                [0.2, 0.5, 0.5, 0.5, 0.5, 0.5, 0.4, 0.2],
                [0.2, 0.4, 0.5, 0.4, 0.4, 0.4, 0.4, 0.2],
                [0.0, 0.2, 0.2, 0.3, 0.3, 0.2, 0.2, 0.0]]

pawn_scores = [[0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8],
               [0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7, 0.7],
               [0.3, 0.3, 0.4, 0.5, 0.5, 0.4, 0.3, 0.3],
               [0.25, 0.25, 0.3, 0.45, 0.45, 0.3, 0.25, 0.25],
               [0.2, 0.2, 0.2, 0.4, 0.4, 0.2, 0.2, 0.2],
               [0.25, 0.15, 0.1, 0.2, 0.2, 0.1, 0.15, 0.25],
               [0.25, 0.3, 0.3, 0.0, 0.0, 0.3, 0.3, 0.25],
               [0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2, 0.2]]

piece_position_scores = {"wN": knight_scores,
                         "bN": knight_scores[::-1],
                         "wB": bishop_scores,
                         "bB": bishop_scores[::-1],
                         "wQ": queen_scores,
                         "bQ": queen_scores[::-1],
                         "wR": rook_scores,
                         "bR": rook_scores[::-1],
                         "wp": pawn_scores,
                         "bp": pawn_scores[::-1]}

CHECKMATE = 1000
STALEMATE = 0
DEPTH = 3


def findBestMove(game_state, valid_moves, return_queue):
    global next_move
    next_move = None
    random.shuffle(valid_moves)
    # findMoveNegaMaxAlphaBeta(game_state, valid_moves, DEPTH, -CHECKMATE, CHECKMATE,
    #                          1 if game_state.white_to_move else -1)
    
    use_alpha_beta = True
    if use_alpha_beta:
        findMoveAlphaBeta(game_state, valid_moves, DEPTH, -CHECKMATE, CHECKMATE, True)
    else:
        findMoveMinimax(game_state, valid_moves, DEPTH, True)
    return_queue.put(next_move)


# def findMoveNegaMaxAlphaBeta(game_state, valid_moves, depth, alpha, beta, turn_multiplier):
#     global next_move
#     if depth == 0:
#         return turn_multiplier * scoreBoard(game_state)
#     # move ordering - implement later //TODO
#     max_score = -CHECKMATE
#     for move in valid_moves:
#         game_state.makeMove(move)
#         next_moves = game_state.getValidMoves()
#         score = -findMoveNegaMaxAlphaBeta(game_state, next_moves, depth - 1, -beta, -alpha, -turn_multiplier)
#         if score > max_score:
#             max_score = score
#             if depth == DEPTH:
#                 next_move = move
#         game_state.undoMove()
#         if max_score > alpha:
#             alpha = max_score
#         if alpha >= beta:
#             break
#     return max_score

def findMoveMinimax(game_state, valid_moves, depth, maximizingPlayer):
    global next_move
    if depth == 0:
        return scoreBoard(game_state)
    
    if maximizingPlayer:
        max_score = -CHECKMATE
        for move in valid_moves:
            game_state.makeMove(move)
            next_moves = game_state.getValidMoves()
            value = findMoveMinimax(game_state, next_moves, depth - 1, False)
            if value > max_score:
                max_score = value
                if depth == DEPTH:
                    next_move = move
                    
            game_state.undoMove()
        return max_score
    else:
        min_score = CHECKMATE
        for move in valid_moves:
            game_state.makeMove(move)
            next_moves = game_state.getValidMoves()
            min_score = min(min_score, findMoveMinimax(game_state, next_moves, depth - 1, True))
            game_state.undoMove()
        return min_score
    
    
def findMoveAlphaBeta(game_state, valid_moves, depth, alpha, beta, maximizingPlayer):
    global next_move
    if depth == 0:
        return scoreBoard(game_state)
    
    if maximizingPlayer:
        value = -CHECKMATE
        for move in valid_moves:
            game_state.makeMove(move)
            next_moves = game_state.getValidMoves()
            value = max(value, findMoveAlphaBeta(game_state, next_moves, depth - 1, alpha, beta, False))
            game_state.undoMove()
            if value > alpha:
                alpha = value
                if depth == DEPTH:
                    next_move = move
            if alpha >= beta:
                break
        return value
    else:
        value = CHECKMATE
        for move in valid_moves:
            game_state.makeMove(move)
            next_moves = game_state.getValidMoves()
            value = min(value, findMoveAlphaBeta(game_state, next_moves, depth - 1, alpha, beta, True))
            game_state.undoMove()
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value

def findMoveAlphaBeta(game_state, valid_moves, depth, alpha, beta, maximizingPlayer):
    global next_move
    if depth == 0:
        return scoreBoard(game_state)
    
    if maximizingPlayer:
        value = -CHECKMATE
        for move in valid_moves:
            game_state.makeMove(move)
            next_moves = game_state.getValidMoves()
            value = max(value, findMoveAlphaBeta(game_state, next_moves, depth - 1, alpha, beta, False))
            game_state.undoMove()
            if value > alpha:
                alpha = value
                if depth == DEPTH:
                    next_move = move
            if alpha >= beta:
                break
        return value
    else:
        value = CHECKMATE
        for move in valid_moves:
            game_state.makeMove(move)
            next_moves = game_state.getValidMoves()
            value = min(value, findMoveAlphaBeta(game_state, next_moves, depth - 1, alpha, beta, True))
            game_state.undoMove()
            beta = min(beta, value)
            if alpha >= beta:
                break
        return value
    
'''
function alphabeta(node, depth, α, β, maximizingPlayer) is
    if depth == 0 or node is terminal then
        return the heuristic value of node
    if maximizingPlayer then
        value := −∞
        for each child of node do
            value := max(value, alphabeta(child, depth − 1, α, β, FALSE))
            α := max(α, value)
            if value ≥ β then
                break (* β cutoff *)
        return value
    else
        value := +∞
        for each child of node do
            value := min(value, alphabeta(child, depth − 1, α, β, TRUE))
            β := min(β, value)
            if value ≤ α then
                break (* α cutoff *)
        return value
'''

def scoreBoard(game_state):
    """
    Score the board. A positive score is good for black, a negative score is good for white.
    """
    if game_state.checkmate:
        if game_state.white_to_move:
            return CHECKMATE  # black wins
        else:
            return -CHECKMATE  # white wins
    elif game_state.stalemate:
        return STALEMATE #Hòa
    
    score = 0 #Nếu không có tình huống checkmate hay stalemate thì khởi tạo score
    for row in range(len(game_state.board)):
        for col in range(len(game_state.board[row])):
            piece = game_state.board[row][col]
            if piece != "--":
                piece_position_score = 0
                if piece[1] != "K":
                    piece_position_score = piece_position_scores[piece][row][col]
                if piece[0] == "w":
                    score -= piece_score[piece[1]] + piece_position_score
                if piece[0] == "b":
                    score += piece_score[piece[1]] + piece_position_score

    return score


def findRandomMove(valid_moves):
    """
    Picks and returns a random valid move.
    """
    return valid_moves[0]
    # return random.choice(valid_moves)
