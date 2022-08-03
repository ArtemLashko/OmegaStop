import unittest
import chessengine
import chess

class MyTestCase(unittest.TestCase):
    starting_fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"  # starting position

    def test_whose_move(self):
        for i in range(1, 20):  # 20 iteration of a test
            ChessEngine = chessengine.Engine(self.starting_fen)
            for j in range(1, 10):
                if ChessEngine.board.is_game_over():  # we randomly found a mate
                    break
                move = ChessEngine.random_move()
                move = chess.Move.from_uci(move)
                #print(i, j, ChessEngine.whose_move(), move)
                if j % 2 == 1:
                    self.assertEqual(ChessEngine.whose_move(), 'White')
                else:
                    self.assertEqual(ChessEngine.whose_move(), 'Black')
                ChessEngine.board.push(move)  # make a random move


if __name__ == '__main__':
    unittest.main()
