import random
import numpy as np
import os
import time
import sys

def floodFill(x, y): # floodfills an area in order to clear all empty squares around an empty square
    try:
        if markedSquares[y][x] == 0:
            
            if board[y][x] == 0: # check if square is empty
                displayBoard[y][x] = ' '
            else:
                displayBoard[y][x] = board[y][x]

            markedSquares[y][x] = 1
            printBoard()
            
            if board[y + 1][x] == 0:
                floodFill(x, y + 1)
            elif board[y + 1][x] != 'm':
                displayBoard[y + 1][x] = board[y + 1][x]
            
            if board[y - 1][x] == 0 and y - 1 >= 0:
                floodFill(x, y - 1)
            elif board[y - 1][x] != 'm' and y - 1 >= 0:
                displayBoard[y - 1][x] = board[y - 1][x]
            
            if board[y][x + 1] == 0:
                floodFill(x + 1, y)
            elif board[y][x + 1] != 'm':
                displayBoard[y][x + 1] = board[y][x + 1]
            
            if board[y][x - 1] == 0 and x - 1 >= 0:
                floodFill(x - 1, y)
            elif board[y][x - 1] != 'm' and x - 1 >= 0:
                displayBoard[y][x -1] = board[y][x - 1]
        
    except IndexError:
        pass

def clear(x, y): # clear a square 
    global markedSquares
    markedSquares = [[0 for x in range(len(board[0]))] for y in range(len(board))]
    
    if board[y][x] == 'm': # check if mine has been uncovered
        clearBoard()
        printBoard()
        print("You lose!")
        input("Press Enter to continue...")
        sys.exit(0)
    else:
        floodFill(x, y)
    
    printBoard()

    if checkWin() == True: # check if player has won
        clearBoard()
        printBoard()
        print("You win!")
        input("Press Enter to continue...")
        sys.exit(0)

def checkWin(): # check if player has won
    for y in range(len(board)):
        for x in range(len(board[0])):
            if board[y][x] != 'm' and displayBoard[y][x] == '■': # check if there are any squares that aren't mines which still need clearing
                return False
    
    return True

def clearBoard(): # clears the board
    for y in range(len(board)):
        for x in range(len(board[0])):
            displayBoard[y][x] = board[y][x]
            if displayBoard[y][x] == 0:
                displayBoard[y][x] = " "


def printBoard(): # print the board to the screen
    os.system('cls' if os.name == 'nt' else 'clear')

    print(end="  ")
    for i in range(len(displayBoard[0])): # display numbers at top
        print((" " + "%2s" % i).replace(" ", "_"), end = "")
    
    print()

    for i in range(len(displayBoard)):
        print("%2s" % str(i), end=" │") # display numbers at side
        print("%1s" % str(displayBoard[i]).replace("[", "").replace("]", "").replace(",", " ").replace("'", "")) # print rows of board


def mark(x, y): # places a flag on a square
    global flagCounter
    if displayBoard[y][x] == "■" and flagCounter < maxFlags:
        displayBoard[y][x] = "?"
        flagCounter += 1
        printBoard()
    elif flagCounter >= maxFlags and displayBoard[y][x] == "■":
        printBoard()
        print("You have no more flags!")
    elif displayBoard[y][x] == "?" :
        displayBoard[y][x] = "■"
        flagCounter -= 1
        printBoard()
    else:
        printBoard()

def setupBoard(width, height, mines): # initialises board
    board = [[-1 for x in range(width)] for y in range(height)]
    global displayBoard

    print("Generating board...", end="")
    displayBoard = [["■" for x in range(width)] for y in range(height)] # fill displayed board with squares
    print("done")

    print("Placing mines...", end="")
    for i in range(mines): # place mines
        randomLocation = (random.randint(0, height - 1), random.randint(0, width - 1)) # pick random square
        
        while board[randomLocation[0]][randomLocation[1]] == "m": # check if square is already occupied
            randomLocation = (random.randint(0, height - 1), random.randint(0, width - 1)) # pick random square
        
        board[randomLocation[0]][randomLocation[1]] = "m" # place mine
    print("done")
    
    print("Calculating mine counters...", end="")
    for y in range(height): # fill all squares with number of mines around them
        for x in range(width):
            if not board[y][x] == "m": 
                
                mineChecker = 0
                for j in range(-1, 2): # iterate through all squares surrounding selected one
                    for k in range(-1, 2):
                        if 0 <= y + j <= height - 1 and 0 <= x + k <= width - 1: # don't check outside board
                            if board[y + j][x + k] == "m": # check if square is occupied
                                mineChecker += 1
                                
            
                board[y][x] = mineChecker

    print("done")
    return board

difficulty = input("Choose difficulty (beginner, intermediate, expert, custom)/(B/I/E/C): ")

if difficulty == "beginner" or difficulty == "B": # set up board size based on selected difficulty
    board = setupBoard(8, 8, 10)
    maxFlags = 10
elif difficulty == "intermediate" or difficulty == "I":
    board = setupBoard(16, 16, 40)
    maxFlags = 40
elif difficulty == "expert" or difficulty == "E":
    board = setupBoard(30, 16, 99)
    maxFlags = 99
elif difficulty  == "custom" or difficulty == "C":
    maxFlags = int(input("Enter number of mines: "))
    board = setupBoard(int(input("Enter board width: ")), int(input("Enter board height: ")), maxFlags)
elif difficulty == "ava": # an inside joke, also a board that's easy to solve for debug purposes
    board = setupBoard(3, 3, 1)
else:
    print(difficulty + " is not a valid difficulty!")
    input("Press enter to continue...")
    sys.exit(0)

flagCounter = 0


printBoard()

while 1:
    command = input("mark or clear? (m/c): ")
    inputX = input("x: ")
    inputY = input("y: ")

    try:
        if command == "mark" or command == "m":
            mark(int(inputX), int(inputY))
        elif command == "clear" or command == "c":
            clear(int(inputX), int(inputY))
        elif command == "debug" or command == "d":
            clearBoard()
            printBoard()
        else:
            print("Unknown command!")
    
    except SystemExit:
        sys.exit(0)
    
    except Exception as e:
        printBoard()
        print("Invalid input: " + str(e))
