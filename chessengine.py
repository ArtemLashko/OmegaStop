import chess
import random
from keras.models import load_model
import chess
import numpy as np
import tensorflow


class Engine:
    INF = 99999999999
    NEG_INF = -99999999999
    ML_N = 1  # this constant is used to tune the usage of machine learning

    def __init__(self, fen):
        self.board = chess.Board()
        self.model = load_model("fBIGelo1")  # Machine learning model

        ##########################
        # Values of pieces
        ##########################
        self.pieces = {
            'P': 100,  # Pawn
            'N': 280,  # kNight (because king also has first 'K')
            'B': 310,  # Bishop
            'R': 450,  # Rook
            'Q': 900,  # Queen
            'K': 70000  # King
        }
        ##########################
        # Mapping each piece to a number
        ##########################
        self.pieces_to_number = {
            'P': 1,
            'N': 2,
            'B': 3,
            'R': 4,
            'Q': 5,
            'K': 6
        }
        ##########################
        # Piece-Square tables.
        ##########################
        self.evaluation_tables = {'P': [0, 0, 0, 0, 0, 0, 0, 0,
                                        6, 83, 86, 73, 102, 82, 85, 90,
                                        7, 29, 21, 44, 40, 31, 44, 7,
                                        -17, 16, -2, 15, 14, 0, 15, -13,
                                        -26, 3, 10, 9, 6, 1, 0, -23,
                                        -22, 9, 5, -11, -10, -2, 3, -19,
                                        -31, 8, -7, -37, -36, -14, 3, -31,
                                        0, 0, 0, 0, 0, 0, 0, 0],
                                  'N': [66, -53, -75, -75, -10, -55, -58, -70,
                                        -3, -6, 100, -36, 4, 62, -4, -14,
                                        10, 67, 1, 74, 73, 27, 62, -2,
                                        24, 24, 45, 37, 33, 41, 25, 17,
                                        -1, 5, 31, 21, 22, 35, 2, 0,
                                        -18, 10, 13, 22, 18, 15, 11, -14,
                                        -23, -15, 2, 0, 2, 0, -23, -20,
                                        -74, -23, -26, -24, -19, -35, -22, -69],
                                  'B': [-59, -78, -82, -76, -23, -107, -37, -50,
                                        -11, 20, 35, -42, -39, 31, 2, -22,
                                        -9, 39, -32, 41, 52, -10, 28, -14,
                                        25, 17, 20, 34, 26, 25, 15, 10,
                                        13, 10, 17, 23, 17, 16, 0, 7,
                                        14, 25, 24, 15, 8, 25, 20, 15,
                                        19, 20, 11, 6, 7, 6, 20, 16,
                                        -7, 2, -15, -12, -14, -15, -10, -10],
                                  'R': [35, 29, 33, 4, 37, 33, 56, 50,
                                        55, 29, 56, 67, 55, 62, 34, 60,
                                        19, 35, 28, 33, 45, 27, 25, 15,
                                        0, 5, 16, 13, 18, -4, -9, -6,
                                        -28, -35, -16, -21, -13, -29, -46, -30,
                                        -42, -28, -42, -25, -25, -35, -26, -46,
                                        -53, -38, -31, -26, -29, -43, -44, -53,
                                        -30, -24, -18, 5, -2, -18, -31, -32],
                                  'Q': [6, 1, -8, -104, 69, 24, 88, 26,
                                        14, 32, 60, -10, 20, 76, 57, 24,
                                        -2, 43, 32, 60, 72, 63, 43, 2,
                                        1, -16, 22, 17, 25, 20, -13, -6,
                                        -14, -15, -2, -5, -1, -10, -20, -22,
                                        -30, -6, -13, -11, -16, -11, -16, -27,
                                        -36, -18, 0, -19, -15, -15, -21, -38,
                                        -39, -30, -31, -13, -31, -36, -34, -42],
                                  'K': [4, 54, 47, -99, -99, 60, 83, -62,
                                        -32, 10, 55, 56, 56, 55, 10, 3,
                                        -62, 12, -57, 44, -67, 28, 37, -31,
                                        -55, 50, 11, -4, -19, 13, 0, -49,
                                        -55, -43, -52, -28, -51, -47, -8, -50,
                                        -47, -42, -43, -79, -64, -32, -29, -32,
                                        -4, 3, -14, -50, -57, -18, 13, 4,
                                        17, 30, -3, -14, 6, -1, 40, 18],
                                  }
        self.board.set_fen(fen)  # Initialize the board with a fen string

    # The purpose of this function is to give some board configuration an evaluation
    #  in terms of pawns and position
    def position_eval(self):
        score = 0
        # Chess library interpreter "WHITE" color as True, and "BLACK" as False
        for piece_type in self.pieces.keys():
            score += len(self.board.pieces(self.pieces_to_number[piece_type], True)) * self.pieces[piece_type]
            score -= len(self.board.pieces(self.pieces_to_number[piece_type], False)) * self.pieces[piece_type]
            # Utilize Piece-Square tables for calculating a position advantage
            for ind in self.board.pieces(self.pieces_to_number[piece_type], False):
                score += self.evaluation_tables[piece_type][-ind]
            for ind in self.board.pieces(self.pieces_to_number[piece_type], True):
                score += self.evaluation_tables[piece_type][ind]
        return score

    # Performs minimax on a board
    # Requires 3 parameters
    # board - current chess board, depth - how many "layers" of recursion we have left
    # maxormin - on this particular layer, do we try to maximize evaluation or minimize
    # Human player tries to maximize, and an agent tries to minimize.
    # Returns the best tactical chess move for any position
    # The recommended depth is 4 - 5 since minimax without optimizations
    def minimax(self, depth, mx_depth):
        whiteturn = self.board.turn  # is it a white move 1 - if it's 0 if it's not
        legal_moves = list(self.board.legal_moves)  # list of legal moves for a given position
        bestmove = "" if len(legal_moves) == 0 else str(legal_moves[0])  # this is the best move in string format

        if depth == 0 or self.board.is_game_over():  # the game is over,or we don't want to look anymore
            return self.position_eval()

        # If it is a white turn, we want to maximize a score. If it is black, we want to minimize
        if whiteturn:
            max_score = self.NEG_INF
        else:
            max_score = self.INF

        # Let's iterate over potential moves and investigate opportunities
        for move in legal_moves:
            self.board.push(move)
            temp_score = self.minimax(depth - 1, mx_depth)
            self.board.pop()

            if (whiteturn == 1) and (temp_score > max_score):
                bestmove = str(move)
                max_score = temp_score
            if (whiteturn == 0) and (temp_score < max_score):
                bestmove = str(move)
                max_score = temp_score
            if depth == mx_depth:
                print("Potential answer is " + str(move) + " : " + str(temp_score))
        if depth == mx_depth:
            print(self.whose_move())
            print("Answer is " + str(bestmove) + " : " + str(max_score))
            return bestmove
        return max_score

    def alphabeta(self, depth, mx_depth, alpha, beta, last_move=""):
        whiteturn = int(self.board.turn)  # is it a white move 1 - if it's 0 if it's not
        legal_moves = list(self.board.legal_moves)  # list of legal moves for a given position
        bestmove = "" if len(legal_moves) == 0 else str(legal_moves[0])  # this is the best move in string format

        if depth == 0 or self.board.is_game_over():  # the game is over,or we don't want to look anymore
            return self.position_eval()

        # If it is a white turn, we want to maximize a score. If it is black we want to minimize
        if whiteturn:
            max_score = self.NEG_INF
        else:
            max_score = self.INF

        # On top layers, I want to utilize machine learning to go only into positions that lead to a potential win
        if mx_depth - depth <= self.ML_N:
            lst = []
            for move in legal_moves:
                self.board.push(move)
                lst.append([self.ml_eval(), move])
                self.board.pop()
            if whiteturn:  # that's a white move, and we are interested in maximizing evaluation
                lst.sort(reverse=True, key = lambda x: x[0])
            else:  # that's a black move, and we are interested in minimizing evaluation
                lst.sort(key = lambda x: x[0])
            #print(len(lst))
            legal_moves = []
            for i in range(len(lst)):
                legal_moves.append(lst[i][1])

        # Let's iterate over potential moves and investigate opportunities
        for move in legal_moves:
            self.board.push(move)
            temp_score = self.alphabeta(depth - 1, mx_depth, alpha, beta, str(move))
            self.board.pop()

            if (whiteturn == 1) and (temp_score > max_score):
                bestmove = str(move)
                max_score = temp_score
            if (whiteturn == 0) and (temp_score < max_score):
                bestmove = str(move)
                max_score = temp_score
            if whiteturn == 1:
                alpha = max(alpha, max_score)
            else:
                beta = min(beta, max_score)
            if beta <= alpha:
                return max_score
            if depth == mx_depth:
                print("Potential answer is " + str(move) + " : " + str(temp_score))
        if depth == mx_depth:
            print(self.whose_move())
            print("Answer is " + str(bestmove) + " : " + str(max_score))
            return bestmove
        return max_score

    # Return a random possible move
    def random_move(self):
        return str(random.choice(list(self.board.legal_moves)))

    def minimax_move(self):
        return self.minimax(4, 4)

    # This function transforms a chess position into an input for a Machine Learning model
    # The model has 772 parameters for each color and figures what squares are not free
    # 772 = 2 colors * 6 figures * 8 columns * 8 rows + can white castle + can black castle + who can move
    def make_a_row(self):
        lst = [0 for i in range(2 * 6 * 8 * 8)]
        half = 772 / 2
        for i in range(1, 7):
            for x in self.board.pieces(i, False):  # black color
                lst[0 + (i - 1) * 64 + x] = 1
            for x in self.board.pieces(i, True):  # white color
                lst[half + (i - 1) * 64 + x] = 1
        lst.append(int(self.board.has_castling_rights(True)))
        lst.append(int(self.board.has_castling_rights(False)))
        lst.append(int(self.board.turn))
        return lst

    # This function uses a machine learning model to answer who has an advantage in any given board.
    # 0 - if black has an advantage >= 1.5 pawns, 1 - if it's a draw (-1.5, 1.5), 2 - if white has >= 1.5 pawns
    def ml_eval(self):
        input_list = self.make_a_row()
        output = self.model(np.array([input_list, ]))
        # print(output.numpy().tolist()[0])
        valid = [float(x) for x in output.numpy().tolist()[0]]
        mx = 0  # maximum probability
        mx_ind = 0  # answer

        for i in range(len(valid)):
            if valid[i] > mx:
                mx = valid[i]
                mx_ind = i
        return mx_ind

    # Runs an alphabeta algorithm
    def alphabeta_move(self):
        return self.alphabeta(4,4, self.NEG_INF, self.INF)

    # It returns white if it's a white move. Black otherwise.
    def whose_move(self):
        return "White" if self.board.turn else "Black"

    # Prints debug information.
    def debug(self):
        print("##########################")
        print("FEN = " + str(self.board.fen()))
        print("Turn = " + str(self.whose_move()))
        print("# of moves = " + str(self.board.fullmove_number))
        print("Evaluation = " + str(self.position_eval()))
        print("##########################")


if __name__ == "__main__":
    test = Engine("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    # test.random_move()
    # test.position_eval()
