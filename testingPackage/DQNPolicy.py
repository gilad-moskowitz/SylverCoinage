import random
import numpy as np

class AbstractDQNPolicy:
    def __init__(self):
        pass
    
    def get_action(self, q_values, warm_up, mask):
        return random.randint(0, len(q_values))

class EpsilonGreedyPolicy(AbstractDQNPolicy):
    def __init__(self, epsilon=0.05, decay_rate=0.999, min_epsilon=0.01):
        self.epsilon = epsilon
        self.decay_rate = decay_rate
        self.min_epsilon = min_epsilon
    
    def get_action(self, q_values, warm_up, mask):
        assert len(q_values[0]) == len(mask), "Mask array and Q values are not the same size"
        if not warm_up:
            new_epsilon = self.epsilon * self.decay_rate
            if new_epsilon > self.min_epsilon:
                self.epsilon = new_epsilon
        p = random.random()
        if p > self.epsilon:
            action = np.argmax(q_values*mask)
        else:
            legal_moves = [i for i in range(len(q_values[0])) if mask[i] == 1]
            action = random.choice(legal_moves)
        return action