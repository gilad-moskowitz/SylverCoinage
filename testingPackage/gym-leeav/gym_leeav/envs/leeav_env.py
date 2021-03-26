import random
import json
import gym
from gym import spaces
import pandas as pd
import numpy as np
import random
from under200.testingBot import testBot
from numericalSemigroupLite import *

def legalMove(move, movesPlayed, remainingGaps = []):
    if ((type(move) != int) or move < 1):
        return False
    if (move in remainingGaps):
        return True
    if((len(remainingGaps) > 0) and (move not in remainingGaps)):
        return False
    if (len(movesPlayed) == 0):
        return True
    S = NumericalSemigroup(movesPlayed)
    return (move not in S)

MAX_NUM_MOVES = 10000 #Max INT ?
MAX_ACTION = 100 #Max INT ?
MAX_FIRST_MOVE = 37 # per Gilad
MAX_OPPONENT_ACTION = 100000
MAX_OBS = 100000

class LeeavEnv(gym.Env):
    def __init__(self, keep_score=False, name=""):
        super(LeeavEnv, self).__init__()
        self.action_space = spaces.Discrete(MAX_ACTION)
#         self.observation_space = spaces.Box(low=0, high=MAX_ACTION, shape=(MAX_NUM_MOVES*2,), dtype=np.int64)
        self.observation_space = spaces.Box(
            low=0, high=MAX_OPPONENT_ACTION, shape=(2, MAX_NUM_MOVES), dtype=np.float64)
        self.save_name = name
        self.worst_performance = 0
        if keep_score:
            self.score = [0,0]
            self.last_n_games = []
            self.best_performance = 0
        else:
            self.score = []
            self.last_n_games = []
            self.best_performance = 0
    
    def reset(self):
        self.turn = np.random.randint(-1,1)
        self.prev_moves = []
        self.remainingGaps = []
        self.my_illegal_moves = 0
        self.opponent_illegal_moves = 0
        self.winner = "temp"
        self.i_made_illegal_move = False
        return self._nextObservation()
    
    def reset_score(self):
        self.score = [0,0]
        self.last_n_games = []
        self.best_performance = 0
    
    def _nextObservation(self): # fix second move for my bot
        if len(self.prev_moves) == 0:
            if self.turn == -1:
                print("testbot starts")
                move = testBot().nextMove([], [], 100)
                legal = self._takeAction(move) # do something if not legal?
                while not legal:
                    print("testbot made an illegal move: ", move)
                    self.opponent_illegal_moves += 1
                    if self.opponent_illegal_moves == 3:
                        break
                    move = testBot().nextMove([], [])
                    legal = self._takeAction(move)
                obs = [[move] + [0 for i in range(MAX_NUM_MOVES - 1)], [0 for i in range(MAX_NUM_MOVES)]]
            else: # Currently using a random first move
                print("I start")
                move = random.choice([5, 7, 11, 13, 17, 19, 23, 29, 31, 37])
                legal = self._takeAction(move) # do something if not legal?
                while not legal:
#                     print("I made an illegal move: ", move)
                    self.my_illegal_moves += 1
                    if self.my_illegal_moves == 3:
                        break
                    move = np.random.randint(5, MAX_FIRST_MOVE)
                    legal = self._takeAction(move)
                obs = [[move] + [0 for i in range(MAX_NUM_MOVES - 1)], [0 for i in range(MAX_NUM_MOVES)]]
        else:
            if not self.i_made_illegal_move:
                move = testBot().nextMove(self.prev_moves, self.remainingGaps, 100)
                legal = self._takeAction(move) # do something if not legal?
                while not legal:
                    self.opponent_illegal_moves += 1
                    if self.opponent_illegal_moves == 3:
                        break
                    move = testBot().nextMove(self.prev_moves, self.remainingGaps, 100)
                    legal = self._takeAction(move)
            obs = [self.prev_moves + [0 for i in range(MAX_NUM_MOVES - len(self.prev_moves))], self.remainingGaps + [0 for i in range(MAX_NUM_MOVES - len(self.remainingGaps))]]
        return np.array(obs)
    
    def step(self, action):
        # Try rewarding odd number of remaining gaps, as well as higher reward for less remaining gaps
        reward = 0
        prevGaps = self.remainingGaps
        if self.turn == 0:
            self.turn = -1
            return self._nextObservation(), 0, False, {}
        done = False
        if self.prev_moves[-1] == 1:
            reward = 10 # reward = 150
            self.winner = "Me!"
            done = True
        if self.opponent_illegal_moves == 3:
            self.winner = "Me!"
            reward = 0
            done = True
        if not done:
            legal = self._takeAction(action)
            if not legal:
                print("I made an illegal move: ", action)
                print(self.prev_moves)
                reward = 0
                self.my_illegal_moves += 1
                self.i_made_illegal_move = True
                if self.my_illegal_moves == 100:
                    self.winner = "Not me :("
                    reward = -150
                    done = True
                    
            else:
                if action == 1:
                    self.winner = "Not me :("
                    reward = -10
                    done = True
#                 self.i_made_illegal_move = False
#                 if action not in [1, 2, 3]:
#                     num_remgaps = len(self.remainingGaps)
#                     if action in prevGaps:
#                         if num_remgaps <= 50:
#                             if num_remgaps % 2 == 1:
#                                 reward = len(self.remainingGaps)
#                             else:
#                                 reward = 30
#                         else:
#                             reward = 20
#                     elif len(prevGaps) == 0:
#                         if num_remgaps <= 50:
#                             if num_remgaps % 2 == 1:
#                                 reward = len(self.remainingGaps)
#                             else:
#                                 reward = 30
#                         else:
#                             reward = 20
#                     else:
#                         print("something went wrong")
#                         print(action)
#                         reward = 0
#                 else:
#                     print("RG: ", len(prevGaps))
#                     if len(prevGaps) == 1:
#                         self.winner = "Not me :( BUT I played correctly"
#                         reward = 10
#                     else:
#                         self.winner = "Not me :("
#                         reward = -300
#                     done = True
                
        if not done:
            obs = self._nextObservation()
        else:
            obs = [self.prev_moves + [0 for i in range(MAX_NUM_MOVES - len(self.prev_moves))], self.remainingGaps + [0 for i in range(MAX_NUM_MOVES - len(self.remainingGaps))]]
            obs = np.array(obs)
        return obs, reward, done, {}
    
    def _takeAction(self, action):
        move = int(action)
        legal = legalMove(move, self.prev_moves, self.remainingGaps)
        if not legal:
            return legal
        self.prev_moves.append(move)
        if (gcd_list(self.prev_moves) == 1):
            if (len(self.remainingGaps) == 0):
                S1 = NumericalSemigroup(self.prev_moves)
                self.remainingGaps = S1.gaps
            else:
                current_linear_combos = [i for i in range(0, max(self.remainingGaps)) if (i not in self.remainingGaps)]
                newGaps = []
                for i in self.remainingGaps:
                    i_stays = True
                    for j in current_linear_combos:
                        if((i - j) >= 0) and ((i-j)%move == 0):
                            i_stays = False
                            break
                        else:
                            continue
                    if (i_stays):
                        newGaps.append(i)
                self.remainingGaps = [i for i in newGaps]
        return legal

    def render(self, mode='human'):
        if self.winner != "temp":
            if self.score:
                if self.winner == "Me!":
                    self.score[0] += 1
                    self.last_n_games.append(0)
                else:
                    self.score[1] += 1
                    self.last_n_games.append(1)
                print("Current score: ", self.score)
            print(self.save_name + " Winner: " + self.winner)
            print("Number of MY illegal moves: ", self.my_illegal_moves)
            print("Number of OPP illegal moves: ", self.opponent_illegal_moves)
            if len(self.last_n_games) == 50:
                avg = (50 - sum(self.last_n_games)) / 50
                if self.best_performance < avg:
                    self.best_performance = avg
                print("Rolling avg win percentage (last 50 games): ", avg)
                print("Rolling avg win percentage (max): ", self.best_performance)
                self.last_n_games.pop(0)
            print(self.prev_moves)
