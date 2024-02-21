import random
import time
import pygame
import math
import numpy as np
from connect4 import connect4
from copy import deepcopy


class connect4Player(object):
	def __init__(self, position, seed=0, CVDMode=False):
		self.position = position
		self.opponent = None
		self.seed = seed
		random.seed(seed)
		if CVDMode:
			global P1COLOR
			global P2COLOR
			P1COLOR = (227, 60, 239)
			P2COLOR = (0, 255, 0)

	def play(self, env: connect4, move: list) -> None:
		move = [-1]

class human(connect4Player):

	def play(self, env: connect4, move: list) -> None:
		move[:] = [int(input('Select next move: '))]
		while True:
			if int(move[0]) >= 0 and int(move[0]) <= 6 and env.topPosition[int(move[0])] >= 0:
				break
			move[:] = [int(input('Index invalid. Select next move: '))]

class human2(connect4Player):

	def play(self, env: connect4, move: list) -> None:
		done = False
		while(not done):
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()

				if event.type == pygame.MOUSEMOTION:
					pygame.draw.rect(screen, BLACK, (0,0, width, SQUARESIZE))
					posx = event.pos[0]
					if self.position == 1:
						pygame.draw.circle(screen, P1COLOR, (posx, int(SQUARESIZE/2)), RADIUS)
					else: 
						pygame.draw.circle(screen, P2COLOR, (posx, int(SQUARESIZE/2)), RADIUS)
				pygame.display.update()

				if event.type == pygame.MOUSEBUTTONDOWN:
					posx = event.pos[0]
					col = int(math.floor(posx/SQUARESIZE))
					move[:] = [col]
					done = True

class randomAI(connect4Player):

	def play(self, env: connect4, move: list) -> None:
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		move[:] = [random.choice(indices)]

class stupidAI(connect4Player):

	def play(self, env: connect4, move: list) -> None:
		possible = env.topPosition >= 0
		indices = []
		for i, p in enumerate(possible):
			if p: indices.append(i)
		if 3 in indices:
			move[:] = [3]
		elif 2 in indices:
			move[:] = [2]
		elif 1 in indices:
			move[:] = [1]
		elif 5 in indices:
			move[:] = [5]
		elif 6 in indices:
			move[:] = [6]
		else:
			move[:] = [0]

class minimaxAI(connect4Player):
	def __init__(self, position, seed, CVDMode=False, depth=4):
		super().__init__(position, seed, CVDMode)  # Initialize the base class
		self.depth = depth
	
	def play(self, env, move: list) -> None:
		_, chosen_move = self.minimax(env, self.depth, True)
		move[0] = chosen_move

	def minimax(self, env, depth, maximizingPlayer):
		if depth == 0:
			return self.eval_function(env.board), None
		
		possible_moves = [i for i, p in enumerate(env.topPosition) if p >= 0]
		
		if not possible_moves:
			return 0, None	# Game is a draw or the board is full

		if maximizingPlayer:
			maxEval = float('-inf')
			best_move = None
			for move in possible_moves:
				env_copy = deepcopy(env)
				self.simulateMove(env_copy, move, self.position)
				if env_copy.gameOver(move, self.position):
					return float('inf'), move  # Immediate win
				eval, _ = self.minimax(env_copy, depth-1, False)
				if eval > maxEval:
					maxEval = eval
					best_move = move
			return maxEval, best_move
		else:
			minEval = float('inf')
			best_move = None
			opponent_position = 1 if self.position == 2 else 2
			for move in possible_moves:
				env_copy = deepcopy(env)
				self.simulateMove(env_copy, move, opponent_position)
				if env_copy.gameOver(move, opponent_position):
					return float('-inf'), move	# Immediate loss
				eval, _ = self.minimax(env_copy, depth-1, True)
				if eval < minEval:
					minEval = eval
					best_move = move
			return minEval, best_move
	
	def simulateMove(self, env, move: int, player: int):
		env.board[env.topPosition[move]][move] = player
		env.topPosition[move] -= 1
		env.history.append(move)

	def eval_function(self, board):
		weight_matrix = np.array([
			[4, 5, 6, 8, 6, 5, 4],	
			[5, 7, 9, 11, 9, 7, 5], 
			[6, 9, 12, 14, 12, 9, 6],
			[6, 9, 12, 14, 12, 9, 6],
			[5, 7, 9, 11, 9, 7, 5],
			[4, 5, 6, 8, 6, 5, 4]
		])
  
		board_array = np.array(board)
		opponent_position = 1 if self.position == 2 else 2
  
		player_score = np.sum(weight_matrix * (board_array == self.position))
		opponent_score = np.sum(weight_matrix * (board_array == opponent_position))
		return player_score - opponent_score


class alphaBetaAI(connect4Player):
	def __init__(self, position, seed=0, CVDMode=False, depth=4):
		super().__init__(position, seed, CVDMode)
		self.depth = depth

	def play(self, env, move: list) -> None:
		_, chosen_move = self.minimax(env, self.depth, True, float('-inf'), float('inf'))
		move[0] = chosen_move

	def minimax(self, env, depth, maximizingPlayer, alpha, beta):
		if depth == 0:
			return self.eval_function(env.board), None
		
		possible_moves = [i for i, p in enumerate(env.topPosition) if p >= 0]
		
		if not possible_moves:
			return 0, None	# Game is a draw or the board is full

		if maximizingPlayer:
			maxEval = float('-inf')
			best_move = None
			for move in possible_moves:
				env_copy = deepcopy(env)
				self.simulateMove(env_copy, move, self.position)
				if env_copy.gameOver(move, self.position):
					return float('inf'), move  # Immediate win
				eval, _ = self.minimax(env_copy, depth-1, False, alpha, beta)
				if eval > maxEval:
					maxEval = eval
					best_move = move
				alpha = max(alpha, eval)
				if beta <= alpha:
					break  # Beta cut-off
			return maxEval, best_move
		else:
			minEval = float('inf')
			best_move = None
			opponent_position = 1 if self.position == 2 else 2
			for move in possible_moves:
				env_copy = deepcopy(env)
				self.simulateMove(env_copy, move, opponent_position)
				if env_copy.gameOver(move, opponent_position):
					return float('-inf'), move	# Immediate loss
				eval, _ = self.minimax(env_copy, depth-1, True, alpha, beta)
				if eval < minEval:
					minEval = eval
					best_move = move
				beta = min(beta, eval)
				if beta <= alpha:
					break  # Alpha cut-off
			return minEval, best_move

	def simulateMove(self, env, move: int, player: int):
		env.board[env.topPosition[move]][move] = player
		env.topPosition[move] -= 1
		if hasattr(env, 'history'):
			env.history.append(move)

	def eval_function(self, board):
		weight_matrix = np.array([
			[3, 4, 5, 7, 5, 4, 3],
			[4, 6, 8, 10, 8, 6, 4],
			[5, 8, 11, 13, 11, 8, 5],
			[5, 8, 11, 13, 11, 8, 5],
			[4, 6, 8, 10, 8, 6, 4],
			[3, 4, 5, 7, 5, 4, 3]
		])
		board_array = np.array(board)
		player_score = np.sum(weight_matrix * (board_array == self.position))
		opponent_position = 1 if self.position == 2 else 2
		opponent_score = np.sum(weight_matrix * (board_array == opponent_position))
		return player_score - opponent_score

# class alphaBetaAI(connect4Player):
# 	def __init__(self, position, seed=0, CVDMode=False, depth=4):
# 		super().__init__(position, seed, CVDMode)
# 		self.depth = depth

# 	def play(self, env, move: list) -> None:
# 		_, chosen_move = self.minimax(env, self.depth, True, float('-inf'), float('inf'))
# 		move[0] = chosen_move
	
# 	def minimax(self, env, depth, maximizingPlayer, alpha, beta):
# 		if depth == 0:
# 			return self.eval_function(env.board), None

# 		if not [i for i, p in enumerate(env.topPosition) if p >= 0]:
# 			return 0, None	# Game is a draw or the board is full

# 		if maximizingPlayer:
# 			return self.maximize(env, depth, alpha, beta)
# 		else:
# 			return self.minimize(env, depth, alpha, beta)

	
# 	def maximize(self, env, depth, alpha, beta):
# 		maxEval = float('-inf')
# 		best_move = None
# 		possible_moves = [i for i, p in enumerate(env.topPosition) if p >= 0]
		
# 		for move in possible_moves:
# 			env_copy = deepcopy(env)
# 			self.simulateMove(env_copy, move, self.position)
# 			if env_copy.gameOver(move, self.position):
# 				return float('inf'), move  # Immediate win
# 			eval, _ = self.minimax(env_copy, depth - 1, False, alpha, beta)
# 			if eval > maxEval:
# 				maxEval = eval
# 				best_move = move
# 			alpha = max(alpha, eval)
# 			if beta <= alpha:
# 				break  # Beta cut-off
# 		return maxEval, best_move

# 	def minimize(self, env, depth, alpha, beta):
# 		minEval = float('inf')
# 		best_move = None
# 		opponent_position = 1 if self.position == 2 else 2
# 		possible_moves = [i for i, p in enumerate(env.topPosition) if p >= 0]
		
# 		for move in possible_moves:
# 			env_copy = deepcopy(env)
# 			self.simulateMove(env_copy, move, opponent_position)
# 			if env_copy.gameOver(move, opponent_position):
# 				return float('-inf'), move	# Immediate loss
# 			eval, _ = self.minimax(env_copy, depth - 1, True, alpha, beta)
# 			if eval < minEval:
# 				minEval = eval
# 				best_move = move
# 			beta = min(beta, eval)
# 			if beta <= alpha:
# 				break  # Alpha cut-off
# 		return minEval, best_move

# 	def simulateMove(self, env, move: int, player: int):
# 		env.board[env.topPosition[move]][move] = player
# 		env.topPosition[move] -= 1
# 		if hasattr(env, 'history'):
# 			env.history.append(move)
	
# 	def eval_function(self, board):
# 		weight_matrix = np.array([
# 			[3, 4, 5, 7, 5, 4, 3],
# 			[4, 6, 8, 10, 8, 6, 4],
# 			[5, 8, 11, 13, 11, 8, 5],
# 			[5, 8, 11, 13, 11, 8, 5],
# 			[4, 6, 8, 10, 8, 6, 4],
# 			[3, 4, 5, 7, 5, 4, 3]
# 		])
# 		board_array = np.array(board)
# 		player_score = np.sum(weight_matrix * (board_array == self.position))
# 		opponent_position = 1 if self.position == 2 else 2
# 		opponent_score = np.sum(weight_matrix * (board_array == opponent_position))
# 		return player_score - opponent_score



SQUARESIZE = 100
BLUE = (0,0,255)
BLACK = (0,0,0)
P1COLOR = (255,0,0)
P2COLOR = (255,255,0)

ROW_COUNT = 6
COLUMN_COUNT = 7

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT+1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE/2 - 5)

screen = pygame.display.set_mode(size)




