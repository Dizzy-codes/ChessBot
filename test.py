import chess
board = chess.Board()

dict = {"Michael": 10, "Sarah": 80, "Austin": 35}
print(sorted(dict, key=dict.get, reverse=True)[:2])