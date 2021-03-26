import numpy as np
from numericalSemigroupLite import NumericalSemigroup

class AbstractProcessor:
    def __init__(self):
        pass
    
    def process_observation(self, observation):
        return observation

    def process_action(self, action):
        return action
    
    def get_legal_moves(self, observation, num_actions):
        return np.ones(num_actions)
    
class CartPoleProcessor(AbstractProcessor):
    def process_observation(self, observation):
        return np.array([[observation]])
    
    def process_action(self, action):
        return action
    
    def get_legal_moves(self, observation, num_actions):
        return np.ones(num_actions)
    
class SylverCoinageProcessor(AbstractProcessor):
    def __init__(self, max_observation):
        self.max_observation = max_observation
    
    def process_observation(self, observation):
        return np.array([[observation]]) / self.max_observation
    
    def process_action(self, action):
        if action == 0:
            action = 1
        return action
    
    def get_legal_moves(self, observation, num_actions):
        legal_moves = np.zeros(num_actions)
        if 1 not in observation[0]:
            if 2 not in observation[0] and 3 not in observation[0]:
                mask = [i for i in observation[1] if i < num_actions  and i > 3]
                if mask:
                    legal_moves[mask] = 1
                else:
                    mask = NumericalSemigroup([i for i in observation[0] if i != 0])
                    mask = [i for i in range(num_actions) if i not in mask and i > 3]
                    if mask:
                        legal_moves[mask] = 1
                    else:
                        legal_moves[[1,2,3]] = 1
            elif 2 not in observation[0]:
                legal_moves[2] = 1
            elif 3 not in observation[0]:
                legal_moves[3] = 1
            else:
                legal_moves[1] = 1
        else:
            legal_moves[1:num_actions] = 1
        return legal_moves