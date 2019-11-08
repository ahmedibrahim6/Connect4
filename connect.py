import math
import random
import numpy as np
from pdb import set_trace as breakpoint

def printState(gameState):
	state = np.flip(gameState, 0)
	print("\n")
	for row in state:
		for disc in row:
			if disc == 0:
				print("-", end= '  ')
			if disc == 1:
				print("O", end= '  ')
			if disc == 2:
				print("X", end= '  ')
		print("\n")
	for i in range(1,8):
		print(i, end= '  ')
	print("\n \n \n")


def dsicPlacement(gameState, row, col, disc):
	gameState[row][col] = disc


def getEmptySlot(gameState, col):
	for row in range(ROWS):
		if gameState[row][col] == 0:
			return row



def isSafeMove(gameState, col):
	if  col < 0 or col > 6 :
		return False
	if gameState[ROWS-1][col] == 0:
		return True
	else:
		return False



def get_correctMoves(gameState):
	correctMoves = []
	for column in range(COLS):
		if isSafeMove(gameState, column):
			correctMoves.append(column)
	return correctMoves

def winning_move(gameState, disc):	
	for c in range(COLS-3):
		for r in range(3, ROWS):
			if gameState[r][c] == disc and gameState[r-1][c+1] == disc and gameState[r-2][c+2] == disc and gameState[r-3][c+3] == disc:
				return True

	for c in range(COLS-3):
		for r in range(ROWS):
			if gameState[r][c] == disc and gameState[r][c+1] == disc and gameState[r][c+2] == disc and gameState[r][c+3] == disc:
				return True
	
	for c in range(COLS-3):
		for r in range(ROWS-3):
			if gameState[r][c] == disc and gameState[r+1][c+1] == disc and gameState[r+2][c+2] == disc and gameState[r+3][c+3] == disc:
				return True

	for c in range(COLS):
		for r in range(ROWS-3):
			if gameState[r][c] == disc and gameState[r+1][c] == disc and gameState[r+2][c] == disc and gameState[r+3][c] == disc:
				return True
	
def evaluation(window, disc):	
	score = 0
	opp_disc = disc_PLAYER


	if disc == disc_PLAYER:
		opp_disc = disc_AI

	if window.count(disc) == 4:
		score += 99
	elif window.count(disc) == 3 and window.count(0) == 1:
		score += 5
	elif window.count(disc) == 2 and window.count(0) == 2:
		score += 2

	if window.count(opp_disc) == 3 and window.count(0) == 1:
		score -= 4

	return score

def get_score(gameState, disc): 
	score = 0
	arr = []
	arr1 = []
	arr2 = []

	for i in list(gameState[:, COLS//2]) :
		arr.append(int(i))

	a = arr.count(disc)
	score += a * 3

	for row in range(ROWS):
		for i in list(gameState[row,:]) :
			arr1.append(int(i))
		for c in range(COLS-3):
			window = arr1[c:c+4]
			score += evaluation(window, disc)

	
	for c in range(COLS):
		for i in list(gameState[:,c]):
			arr2.append(int(i))
		for row in range(ROWS-3):
			window = arr2[row:row+4]
			score += evaluation(window, disc)

	
	for row in range(ROWS-3):
		for c in range(COLS-3):
			window = [gameState[row+i][c+i] for i in range(4)]
			score += evaluation(window, disc)

	for row in range(ROWS-3):
		for c in range(COLS-3):
			window = [gameState[row+3-i][c+i] for i in range(4)]
			score += evaluation(window, disc)

	return score



def minimax(gameState, ALPHA, BETA, maximizingPlayer, depth):

	correctMoves = get_correctMoves(gameState)

	is_leaf =  ( len(get_correctMoves(gameState)) == 0 ) or winning_move(gameState, disc_AI) or  winning_move(gameState, disc_PLAYER) 
	if depth == 0 or is_leaf:
		if is_leaf:
			if winning_move(gameState, disc_AI):
				return (None, 999999999999999)
			elif winning_move(gameState, disc_PLAYER):
				return (None, -99999999999999)
			else: 
				return (None, 0)
		else: 
			return (None, get_score(gameState, disc_AI))
	if maximizingPlayer:
		num = -math.inf
		column = random.choice(correctMoves)
		for col in correctMoves:
			row = getEmptySlot(gameState, col)
			gameState_ = gameState.copy()
			dsicPlacement(gameState_, row, col, disc_AI)
			new_score = minimax(gameState_, ALPHA, BETA, False, depth-1 )[1]
			if new_score > num:
				num = new_score
				column = col
			ALPHA = max(ALPHA, num)
			if ALPHA >= BETA:
				break
		return column, num

	else: 
		num = math.inf
		column = random.choice(correctMoves)
		for col in correctMoves:
			row = getEmptySlot(gameState, col)
			gameState_ = gameState.copy()
			dsicPlacement(gameState_, row, col, disc_PLAYER)
			new_score = minimax(gameState_, ALPHA, BETA, True , depth-1)[1]
			if new_score < num:
				num = new_score
				column = col
			BETA = min(BETA, num)
			if ALPHA >= BETA:
				break
		return column, num


ROWS = 6
COLS = 7

AI = 1
disc_AI = 2
turn_PLAYER = 0
disc_PLAYER = 1



gameState = np.zeros((ROWS,COLS))
GameOver = 0

printState(gameState)

gameTurn = random.randint(turn_PLAYER, AI)



while (1) :

	if gameTurn == turn_PLAYER:
		print("+===========+")
		print("|Player Turn|")
		print("+===========+ \n")
		col = int(input("Enter the number of column {1,7} : ")) -1

		if isSafeMove(gameState, col):
			row = getEmptySlot(gameState, col)
			dsicPlacement(gameState, row, col, disc_PLAYER)
			gameTurn += 1
			gameTurn = gameTurn % 2
			printState(gameState)
			if winning_move(gameState, disc_PLAYER):
				GameOver = True
				print("Congratulations you win! \n")
		else :
			print("Invalid column number \n")
			gameTurn = turn_PLAYER


	elif gameTurn == AI and not GameOver:				
		col, minimax_score = minimax(gameState, -math.inf, math.inf, True , 6)

		if isSafeMove(gameState, col):
			
			row = getEmptySlot(gameState, col)
			dsicPlacement(gameState, row, col, disc_AI)

			print("+=======+")
			print("|AI Turn|")
			print("+=======+")
			printState(gameState)

			gameTurn += 1
			gameTurn = gameTurn % 2
			if winning_move(gameState, disc_AI):
				GameOver = True
				print("AI has won! :( \n")
	#breakpoint()		
	if GameOver:
		print("Play another game! :) \n\n")
		break