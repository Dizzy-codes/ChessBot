from logging import error
from operator import indexOf
import itertools
from itertools import chain
import chess
import chess.svg
import shelve
import random
import sys
import collections
from collections import Counter
from table import *



def evaluate_board():
    #Seprate board use to evalue the position on the main board
    BOARD_REPLICA = chess.Board()
    #Main chess; the board the players use
    BOARD = chess.Board()
    PLAYER_COLOR_WHITE = True
    first_move = True
    index = 0

    #Value to determine if white made a move
    moved = 0

    #The value of each piece
    CHESS_PIECE_VALUES = {
        chess.PAWN: 100,
        chess.ROOK: 500,
        chess.KNIGHT: 320,
        chess.BISHOP: 330,
        chess.QUEEN: 900,
        chess.KING: 9999999999
    }

    #Stores the index of the move(ie: e2)
    CHESS_SQUARE_INDEX = {}

    #Stores the value of the square spot from the table
    CHESS_SQUARE_VALUE = {}

    #Holds the original value of the square
    ORIGINAL_SQUARE_VALUE = {}

    #Holds the current chess piece
    CURRENT_SQUARE_PIECE = []

    #Contains first moves for the bot
    FIRST_MOVES = ["e2e4"]

    #Ask the user if the want to be BLACK or WHITE
    player_color = input("What color do you want to play as [W]hite or [B]lack? ")


    #While the game is active (NOT ENDED)
    while BOARD.is_checkmate() == False and BOARD.is_stalemate() == False and BOARD.is_insufficient_material() == False and BOARD.can_claim_draw() == False:


        #If the player choose White
        if player_color == "W":
            PLAYER_COLOR_WHITE = True
            player_move = input("Enter you move (Example: e2e4 would be = to Pe4) ")
            BOARD.push_san(player_move)
            BOARD_REPLICA.push_san(player_move)

            #Finds the chess piece on the inputed square
            player_chess_piece = str(BOARD.piece_at(chess.parse_square(player_move[-2:])))
            player_move_index = chess.parse_square(str(player_move)[-2:])

            #Add the original square value based on the piece just moved. NOTE: before incentivizing sqaures occurs
            if player_chess_piece == "P":
                ORIGINAL_SQUARE_VALUE[player_move] = pawntable[player_move_index]
            elif player_chess_piece == "R":
                ORIGINAL_SQUARE_VALUE[player_move] = rookstable[player_move_index]
            elif player_chess_piece == "N":
                ORIGINAL_SQUARE_VALUE[player_move] = knightstable[player_move_index]
            elif player_chess_piece == "B":
                ORIGINAL_SQUARE_VALUE[player_move] = bishopstable[player_move_index]
            elif player_chess_piece == "Q":
                ORIGINAL_SQUARE_VALUE[player_move] = queenstable[player_move_index]
            else:
                ORIGINAL_SQUARE_VALUE[player_move] = kingstable[player_move_index]

            CURRENT_SQUARE_PIECE.append(player_chess_piece)

            print(ORIGINAL_SQUARE_VALUE)

            #Increases a square's value, based on what piece is there
            #NOTE: YOU MUST UPDATE ALL TABLES
            if player_chess_piece == "P":
                pawntable[player_move_index] = pawntable[player_move_index] + CHESS_PIECE_VALUES[chess.PAWN]
                rookstable[player_move_index] = rookstable[player_move_index] + CHESS_PIECE_VALUES[chess.PAWN]
                knightstable[player_move_index] = knightstable[player_move_index] + CHESS_PIECE_VALUES[chess.PAWN]
                bishopstable[player_move_index] = bishopstable[player_move_index] + CHESS_PIECE_VALUES[chess.PAWN]
                queenstable[player_move_index] = queenstable[player_move_index] + CHESS_PIECE_VALUES[chess.PAWN]
                kingstable[player_move_index] = kingstable[player_move_index] + CHESS_PIECE_VALUES[chess.PAWN]
            elif player_chess_piece == "R":
                pawntable[player_move_index] = pawntable[player_move_index] + CHESS_PIECE_VALUES[chess.ROOK]
                rookstable[player_move_index] = rookstable[player_move_index] + CHESS_PIECE_VALUES[chess.ROOK]
                knightstable[player_move_index] = knightstable[player_move_index] + CHESS_PIECE_VALUES[chess.ROOK]
                bishopstable[player_move_index] = bishopstable[player_move_index] + CHESS_PIECE_VALUES[chess.ROOK]
                queenstable[player_move_index] = queenstable[player_move_index] + CHESS_PIECE_VALUES[chess.ROOK]
                kingstable[player_move_index] = kingstable[player_move_index] + CHESS_PIECE_VALUES[chess.ROOK]
            elif player_chess_piece == "N":
                pawntable[player_move_index] = pawntable[player_move_index] + CHESS_PIECE_VALUES[chess.KNIGHT]
                rookstable[player_move_index] = rookstable[player_move_index] + CHESS_PIECE_VALUES[chess.KNIGHT]
                knightstable[player_move_index] = knightstable[player_move_index] + CHESS_PIECE_VALUES[chess.KNIGHT]
                bishopstable[player_move_index] = bishopstable[player_move_index] + CHESS_PIECE_VALUES[chess.KNIGHT]
                queenstable[player_move_index] = queenstable[player_move_index] + CHESS_PIECE_VALUES[chess.KNIGHT]
                kingstable[player_move_index] = kingstable[player_move_index] + CHESS_PIECE_VALUES[chess.KNIGHT]
            elif player_chess_piece == "B":
                pawntable[player_move_index] = pawntable[player_move_index] + CHESS_PIECE_VALUES[chess.BISHOP]
                rookstable[player_move_index] = rookstable[player_move_index] + CHESS_PIECE_VALUES[chess.BISHOP]
                knightstable[player_move_index] = knightstable[player_move_index] + CHESS_PIECE_VALUES[chess.BISHOP]
                bishopstable[player_move_index] = bishopstable[player_move_index] + CHESS_PIECE_VALUES[chess.BISHOP]
                queenstable[player_move_index] = queenstable[player_move_index] + CHESS_PIECE_VALUES[chess.BISHOP]
                kingstable[player_move_index] = kingstable[player_move_index] + CHESS_PIECE_VALUES[chess.BISHOP]
            elif player_chess_piece == "Q":
                pawntable[player_move_index] = pawntable[player_move_index] + CHESS_PIECE_VALUES[chess.QUEEN]
                rookstable[player_move_index] = rookstable[player_move_index] + CHESS_PIECE_VALUES[chess.QUEEN]
                knightstable[player_move_index] = knightstable[player_move_index] + CHESS_PIECE_VALUES[chess.QUEEN]
                bishopstable[player_move_index] = bishopstable[player_move_index] + CHESS_PIECE_VALUES[chess.QUEEN]
                queenstable[player_move_index] = queenstable[player_move_index] + CHESS_PIECE_VALUES[chess.QUEEN]
                kingstable[player_move_index] = kingstable[player_move_index] + CHESS_PIECE_VALUES[chess.QUEEN]
            else:
                pawntable[player_move_index] = pawntable[player_move_index] + CHESS_PIECE_VALUES[chess.KING]
                rookstable[player_move_index] = rookstable[player_move_index] + CHESS_PIECE_VALUES[chess.KING]
                knightstable[player_move_index] = knightstable[player_move_index] + CHESS_PIECE_VALUES[chess.KING]
                bishopstable[player_move_index] = bishopstable[player_move_index] + CHESS_PIECE_VALUES[chess.KING]
                queenstable[player_move_index] = queenstable[player_move_index] + CHESS_PIECE_VALUES[chess.KING]
                kingstable[player_move_index] = kingstable[player_move_index] + CHESS_PIECE_VALUES[chess.KING]


            #Checks if a sqaure value has moved. IF the piece is no longer there, revert the square to its orginal value
            for key, value in ORIGINAL_SQUARE_VALUE.items():
                if BOARD.piece_at(chess.parse_square(key[-2:])) == None or str(BOARD.piece_at(chess.parse_square(key[-2:]))) != CURRENT_SQUARE_PIECE[index]:
                    pawntable[chess.parse_square(str(key[-2:]))] = value
                    rookstable[chess.parse_square(str(key[-2:]))] = value
                    knightstable[chess.parse_square(str(key[-2:]))] = value
                    bishopstable[chess.parse_square(str(key[-2:]))] = value
                    queenstable[chess.parse_square(str(key[-2:]))] = value
                    kingstable[chess.parse_square(str(key[-2:]))] = value
                index += 1

        else:
            PLAYER_COLOR_WHITE = False



                    

        #Makes a random good first move
        if PLAYER_COLOR_WHITE == False and first_move == True:
            random_move = random.choice(FIRST_MOVES)
            BOARD.push_san(random_move)
            BOARD_REPLICA.push_san(random_move)
            print(f"Last move made was {str(BOARD.peek())}")
            print(BOARD)
            first_move = False

        #When the player plays as black
        if PLAYER_COLOR_WHITE == False:
            player_move = input("Enter you move (Example: e2e4 would be = to Pe4) ")
            BOARD.push_san(player_move)
            BOARD_REPLICA.push_san(player_move)
            print(f"Last move made was {str(BOARD.peek())}")
            print(BOARD)
            print(" ")
            

            #Finds the chess piece on the inputed square
            player_chess_piece = str(BOARD.piece_at(chess.parse_square(player_move[-2:])))
            player_move_index = chess.parse_square(str(player_move)[-2:])

            #Add the original square value based on the piece just moved. NOTE: before incentivizing sqaures occurs
            if player_chess_piece == "p":
                ORIGINAL_SQUARE_VALUE[player_move] = pawntable[player_move_index]
            elif player_chess_piece == "r":
                ORIGINAL_SQUARE_VALUE[player_move] = rookstable[player_move_index]
            elif player_chess_piece == "n":
                ORIGINAL_SQUARE_VALUE[player_move] = knightstable[player_move_index]
            elif player_chess_piece == "b":
                ORIGINAL_SQUARE_VALUE[player_move] = bishopstable[player_move_index]
            elif player_chess_piece == "q":
                ORIGINAL_SQUARE_VALUE[player_move] = queenstable[player_move_index]
            else:
                ORIGINAL_SQUARE_VALUE[player_move] = kingstable[player_move_index]

            CURRENT_SQUARE_PIECE.append(player_chess_piece)

            #Increases a square's value, based on what piece is there
            #NOTE: YOU MUST UPDATE ALL TABLES
            if player_chess_piece == "p":
                pawntable[player_move_index] = pawntable[player_move_index] + CHESS_PIECE_VALUES[chess.PAWN]
                rookstable[player_move_index] = rookstable[player_move_index] + CHESS_PIECE_VALUES[chess.PAWN]
                knightstable[player_move_index] = knightstable[player_move_index] + CHESS_PIECE_VALUES[chess.PAWN]
                bishopstable[player_move_index] = bishopstable[player_move_index] + CHESS_PIECE_VALUES[chess.PAWN]
                queenstable[player_move_index] = queenstable[player_move_index] + CHESS_PIECE_VALUES[chess.PAWN]
                kingstable[player_move_index] = kingstable[player_move_index] + CHESS_PIECE_VALUES[chess.PAWN]
            elif player_chess_piece == "r":
                pawntable[player_move_index] = pawntable[player_move_index] + CHESS_PIECE_VALUES[chess.ROOK]
                rookstable[player_move_index] = rookstable[player_move_index] + CHESS_PIECE_VALUES[chess.ROOK]
                knightstable[player_move_index] = knightstable[player_move_index] + CHESS_PIECE_VALUES[chess.ROOK]
                bishopstable[player_move_index] = bishopstable[player_move_index] + CHESS_PIECE_VALUES[chess.ROOK]
                queenstable[player_move_index] = queenstable[player_move_index] + CHESS_PIECE_VALUES[chess.ROOK]
                kingstable[player_move_index] = kingstable[player_move_index] + CHESS_PIECE_VALUES[chess.ROOK]
            elif player_chess_piece == "n":
                pawntable[player_move_index] = pawntable[player_move_index] + CHESS_PIECE_VALUES[chess.KNIGHT]
                rookstable[player_move_index] = rookstable[player_move_index] + CHESS_PIECE_VALUES[chess.KNIGHT]
                knightstable[player_move_index] = knightstable[player_move_index] + CHESS_PIECE_VALUES[chess.KNIGHT]
                bishopstable[player_move_index] = bishopstable[player_move_index] + CHESS_PIECE_VALUES[chess.KNIGHT]
                queenstable[player_move_index] = queenstable[player_move_index] + CHESS_PIECE_VALUES[chess.KNIGHT]
                kingstable[player_move_index] = kingstable[player_move_index] + CHESS_PIECE_VALUES[chess.KNIGHT]
            elif player_chess_piece == "b":
                pawntable[player_move_index] = pawntable[player_move_index] + CHESS_PIECE_VALUES[chess.BISHOP]
                rookstable[player_move_index] = rookstable[player_move_index] + CHESS_PIECE_VALUES[chess.BISHOP]
                knightstable[player_move_index] = knightstable[player_move_index] + CHESS_PIECE_VALUES[chess.BISHOP]
                bishopstable[player_move_index] = bishopstable[player_move_index] + CHESS_PIECE_VALUES[chess.BISHOP]
                queenstable[player_move_index] = queenstable[player_move_index] + CHESS_PIECE_VALUES[chess.BISHOP]
                kingstable[player_move_index] = kingstable[player_move_index] + CHESS_PIECE_VALUES[chess.BISHOP]
            elif player_chess_piece == "q":
                pawntable[player_move_index] = pawntable[player_move_index] + CHESS_PIECE_VALUES[chess.QUEEN]
                rookstable[player_move_index] = rookstable[player_move_index] + CHESS_PIECE_VALUES[chess.QUEEN]
                knightstable[player_move_index] = knightstable[player_move_index] + CHESS_PIECE_VALUES[chess.QUEEN]
                bishopstable[player_move_index] = bishopstable[player_move_index] + CHESS_PIECE_VALUES[chess.QUEEN]
                queenstable[player_move_index] = queenstable[player_move_index] + CHESS_PIECE_VALUES[chess.QUEEN]
                kingstable[player_move_index] = kingstable[player_move_index] + CHESS_PIECE_VALUES[chess.QUEEN]
            else:
                pawntable[player_move_index] = pawntable[player_move_index] + CHESS_PIECE_VALUES[chess.KING]
                rookstable[player_move_index] = rookstable[player_move_index] + CHESS_PIECE_VALUES[chess.KING]
                knightstable[player_move_index] = knightstable[player_move_index] + CHESS_PIECE_VALUES[chess.KING]
                bishopstable[player_move_index] = bishopstable[player_move_index] + CHESS_PIECE_VALUES[chess.KING]
                queenstable[player_move_index] = queenstable[player_move_index] + CHESS_PIECE_VALUES[chess.KING]
                kingstable[player_move_index] = kingstable[player_move_index] + CHESS_PIECE_VALUES[chess.KING]


            #Checks if a sqaure value has moved. IF the piece is no longer there, revert the square to its orginal value
            for key, value in ORIGINAL_SQUARE_VALUE.items():
                if BOARD.piece_at(chess.parse_square(key[-2:])) == None or str(BOARD.piece_at(chess.parse_square(key[-2:]))) != CURRENT_SQUARE_PIECE[index]:
                    pawntable[chess.parse_square(str(key[-2:]))] = value
                    rookstable[chess.parse_square(str(key[-2:]))] = value
                    knightstable[chess.parse_square(str(key[-2:]))] = value
                    bishopstable[chess.parse_square(str(key[-2:]))] = value
                    queenstable[chess.parse_square(str(key[-2:]))] = value
                    kingstable[chess.parse_square(str(key[-2:]))] = value
                index += 1
        else:
            PLAYER_COLOR_WHITE = False

        
        #Find all legal moves and add the move name and sqaure index value into a dict
        for move in list(BOARD.legal_moves):
            #The key is the entire move; we use [2:] to get the destination square
            CHESS_SQUARE_INDEX[str(move)] = chess.parse_square(str(move)[-2:])


        #For every legal move, get the value of its destination square
        for key, value in CHESS_SQUARE_INDEX.items():

            #We need to push the move so that the engine can find the piece
            BOARD_REPLICA.push_san(key)

            #Look for the piece and using the index from the dict; use the table that matches the piece NOTE: List is reversed for black
            #NOTE: P- Pawn, N- Knight, B- Bishop, Q- Queen, K- King

            #Finds the chess piece on the inputed square
            chess_piece = str(BOARD_REPLICA.piece_at(chess.parse_square(key[-2:])))

            #Check and append each move. NOTE: also checks if the square has attackers. For the queen we care about ANY attacker being there. Checks if other pieces can capture rooks or queens ect.
            if PLAYER_COLOR_WHITE == False:
                if chess_piece == "P" and len(BOARD_REPLICA.attackers(chess.WHITE, chess.parse_square(key[-2:]))) > len(BOARD_REPLICA.attackers(chess.BLACK, chess.parse_square(key[-2:]))) or chess_piece == "P" and str(BOARD_REPLICA.piece_at(chess.parse_square(key[-2:]))) == "r" or chess_piece == "P" and str(BOARD_REPLICA.piece_at(chess.parse_square(key[-2:]))) == "q" or chess_piece == "P" and str(BOARD_REPLICA.piece_at(chess.parse_square(key[-2:]))) == "n" or chess_piece == "P" and str(BOARD.piece_at(chess.parse_square(key[-2:]))) == "b" or chess_piece == "P" and str(BOARD.piece_at(chess.parse_square(key[-2:]))) == "p":
                    CHESS_SQUARE_VALUE[key] = pawntable[value]
                elif chess_piece == "R" and len(BOARD_REPLICA.attackers(chess.WHITE, chess.parse_square(key[-2:]))) > len(BOARD_REPLICA.attackers(chess.BLACK, chess.parse_square(key[-2:]))) or str(BOARD_REPLICA.piece_at(chess.parse_square(key[-2:]))) == "r" or str(BOARD_REPLICA.piece_at(chess.parse_square(key[-2:]))) == "q":
                    CHESS_SQUARE_VALUE[key] = rookstable[value]
                elif chess_piece == "N" and len(BOARD_REPLICA.attackers(chess.WHITE, chess.parse_square(key[-2:]))) > len(BOARD_REPLICA.attackers(chess.BLACK, chess.parse_square(key[-2:]))) or str(BOARD_REPLICA.piece_at(chess.parse_square(key[-2:]))) == "r" or str(BOARD_REPLICA.piece_at(chess.parse_square(key[-2:]))) == "q":
                    CHESS_SQUARE_VALUE[key] = knightstable[value]
                elif chess_piece == "B" and len(BOARD_REPLICA.attackers(chess.WHITE, chess.parse_square(key[-2:]))) > len(BOARD_REPLICA.attackers(chess.BLACK, chess.parse_square(key[-2:]))) or str(BOARD_REPLICA.piece_at(chess.parse_square(key[-2:]))) == "r" or str(BOARD_REPLICA.piece_at(chess.parse_square(key[-2:]))) == "q":
                    CHESS_SQUARE_VALUE[key] = bishopstable[value]
                elif chess_piece == "Q" and BOARD_REPLICA.is_attacked_by(chess.BLACK, chess.parse_square(key[-2:])) == False:
                    CHESS_SQUARE_VALUE[key] = queenstable[value]
                elif chess_piece == "K":
                    CHESS_SQUARE_VALUE[key] = kingstable[value]
            else:
                if chess_piece == "p" and len(BOARD_REPLICA.attackers(chess.BLACK, chess.parse_square(key[-2:]))) > len(BOARD_REPLICA.attackers(chess.WHITE, chess.parse_square(key[-2:]))) or str(BOARD_REPLICA.piece_at(chess.parse_square(key[-2:]))) == "R" or str(BOARD_REPLICA.piece_at(chess.parse_square(key[-2:]))) == "Q" or str(BOARD_REPLICA.piece_at(chess.parse_square(key[-2:]))) == "N" or str(BOARD_REPLICA.piece_at(chess.parse_square(key[-2:]))) == "B" or str(BOARD_REPLICA.piece_at(chess.parse_square(key[-2:]))) == "P":
                    CHESS_SQUARE_VALUE[key] = pawntable[value]
                elif chess_piece == "r" and len(BOARD_REPLICA.attackers(chess.BLACK, chess.parse_square(key[-2:]))) > len(BOARD_REPLICA.attackers(chess.WHITE, chess.parse_square(key[-2:]))) or str(BOARD_REPLICA.piece_at(chess.parse_square(key[-2:]))) == "R" or str(BOARD_REPLICA.piece_at(chess.parse_square(key[-2:]))) == "Q":
                    CHESS_SQUARE_VALUE[key] = rookstable[value]
                elif chess_piece == "n" and len(BOARD_REPLICA.attackers(chess.BLACK, chess.parse_square(key[-2:]))) > len(BOARD_REPLICA.attackers(chess.WHITE, chess.parse_square(key[-2:]))) or str(BOARD_REPLICA.piece_at(chess.parse_square(key[-2:]))) == "R" or str(BOARD_REPLICA.piece_at(chess.parse_square(key[-2:]))) == "Q":
                    CHESS_SQUARE_VALUE[key] = knightstable[value]
                elif chess_piece == "b" and len(BOARD_REPLICA.attackers(chess.BLACK, chess.parse_square(key[-2:]))) > len(BOARD_REPLICA.attackers(chess.WHITE, chess.parse_square(key[-2:]))) or str(BOARD_REPLICA.piece_at(chess.parse_square(key[-2:]))) == "R" or str(BOARD_REPLICA.piece_at(chess.parse_square(key[-2:]))) == "Q":
                    CHESS_SQUARE_VALUE[key] = bishopstable[value]
                elif chess_piece == "q" and BOARD_REPLICA.is_attacked_by(chess.WHITE, chess.parse_square(key[-2:])) == False:
                    CHESS_SQUARE_VALUE[key] = queenstable[value]
                elif chess_piece == "k":
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

        #Clears index and values to re populate
        CHESS_SQUARE_INDEX.clear()
        CHESS_SQUARE_VALUE.clear()
        index = 0
        


        

#Checks to see if the main file is running, or a sub file
if __name__ == '__main__':
    evaluate_board()
