from operator import indexOf
from aiohttp import BytesIOPayload

from matplotlib.cbook import index_of
import itertools
from itertools import chain
from  more_itertools import unique_everseen
import chess
import chess.svg
import shelve
import random
import sys
import collections
from collections import Counter
from IPython.display import SVG
from table import *

def evaluate_board():
    #Seprate board use to evalue the position on the main board
    BOARD_REPLICA = chess.Board()
    #Main chess; the board the players use
    BOARD = chess.Board()
    WHITE = True
    first_move = True

    #Value to determine if white made a move
    moved = 0

    #The value of each piece
    CHESS_PIECE_VALUES = {
        chess.PAWN: 100,
        chess.ROOK: 500,
        chess.KNIGHT: 320,
        chess.BISHOP: 330,
        chess.QUEEN: 900,
        chess.KING: 20000
    }

    #Stores the index of the move(ie: e2)
    CHESS_SQUARE_INDEX = {}

    #Stores the value of the square spot from the table
    CHESS_SQUARE_VALUE = {}

    #Contains first moves for the bot
    FIRST_MOVES = ["e2e4", "d2d4", "c2c4", "b1c3", "g1f3"]

    #Ask the user if the want to be BLACK or WHITE
    player_color = input("What color do you want to play as [W]hite or [B]lack? ")


    #While the game is active (NOT ENDED)
    while BOARD.is_checkmate() == False and BOARD.is_stalemate() == False and BOARD.is_insufficient_material() == False and BOARD.can_claim_draw() == False:
        #Changes White's value based on the response
        if player_color == "W":
            WHITE = True
            player_move = input("Enter you move (Example: e2e4 would be = to Pe4) ")
            BOARD.push_san(player_move)
        else:
            WHITE = False


        #Makes a random good first move
        if WHITE == False and first_move == True:
            random_move = random.choice(FIRST_MOVES)
            BOARD.push_san(random_move)
            BOARD_REPLICA.push_san(random_move)
            print(f"Last move made was {str(BOARD.peek())}")
            print(BOARD)
            first_move = False

        #When the player plays as black
        if WHITE == False:
            player_move = input("Enter you move (Example: e2e4 would be = to Pe4) ")
            BOARD.push_san(player_move)
            BOARD_REPLICA.push_san(player_move)
            print(f"Last move made was {str(BOARD.peek())}")
            print(BOARD.attackers(chess.parse_square(player_move)[:-2]))
            print(BOARD)
            print(" ")

        
        #Find all legal moves and add the move name and sqaure index value into a dict
        for move in list(BOARD.legal_moves):
            #The key is the entire move; we use [2:] to get the destination square
            CHESS_SQUARE_INDEX[str(move)] = chess.parse_square(str(move)[-2:])

        #For every legal move, get the value of its destination square
        for key, value in CHESS_SQUARE_INDEX.items():
            
            #FOR THE TEST BOARD
            if WHITE == True and moved == 0:
                BOARD_REPLICA.push_san(player_move)
                moved += 1

            #We need to push the move so that the engine can find the piece
            BOARD_REPLICA.push_san(key)

            #Look for the piece and using the index from the dict; use the table that matches the piece NOTE: List is reversed for black
            #NOTE: P- Pawn, N- Knight, B- Bishop, Q- Queen, K- King  
            if str(BOARD_REPLICA.piece_at(chess.parse_square(key[-2:]))) == "P":
                CHESS_SQUARE_VALUE[key] = pawntable[value]
            elif str(BOARD_REPLICA.piece_at(chess.parse_square(key[-2:]))) == "R":
                CHESS_SQUARE_VALUE[key] = rookstable[value]
            elif str(BOARD_REPLICA.piece_at(chess.parse_square(key[-2:]))) == "N":
                CHESS_SQUARE_VALUE[key] = knightstable[value]
            elif str(BOARD_REPLICA.piece_at(chess.parse_square(key[-2:]))) == "B":
                CHESS_SQUARE_VALUE[key] = bishopstable[value]
            elif str(BOARD_REPLICA.piece_at(chess.parse_square(key[-2:]))) == "Q":
                CHESS_SQUARE_VALUE[key] = queenstable[value]
            else:
                CHESS_SQUARE_VALUE[key] = kingstable[value]

            #Reset after each use
            BOARD_REPLICA.pop()
        #Sort the list from greatest value, to least and select the highest value
        BOARD.push_san(sorted(CHESS_SQUARE_VALUE, key=CHESS_SQUARE_VALUE.get, reverse=True)[0])

        #Allows the test board to make the last move; due to .pop() removing the last move from the test board
        BOARD_REPLICA.push_san(str(BOARD.peek()))
        print(f"Last move made was {str(BOARD.peek())}")
        print(BOARD)
        print(" ")

        #Value to determine if white made a move
        moved = 0

        #Clears index and values to re populate
        CHESS_SQUARE_INDEX.clear()
        CHESS_SQUARE_VALUE.clear()



        



























#Checks to see if the main file is running, or a sub file
if __name__ == '__main__':
    evaluate_board()