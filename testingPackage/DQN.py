import numpy as np
from collections import deque
from rl.util import clone_model
import random

class Transition:
    def __init__(self, current_observation, action, reward, new_observation, done):
        self.current_observation = current_observation
        self.action = action
        self.reward = reward
        self.new_observation = new_observation
        self.done = done
        
    def __str__(self):
        return "Current Observation: {}\nCurrent Action: {}\nReward: {}\nNew Observation: {}\nDone: {}".format(self.current_observation, self.action, self.reward, self.new_observation, self.done)

class DQN:
    def __init__(self, model, env, policy, target_model_update=1, gamma=.99, processor=None):
        self.model = model
        self.target_model = clone_model(self.model)
        self.target_model_update = target_model_update
        self.env = env
        self.processor = processor
        self.gamma = gamma
        self.policy = policy
        
        
    def update_target_model_hard(self):
        self.target_model.set_weights(self.model.get_weights())
        
    def create_targets(self, batch_sample, mini_batch_size):
        y = self.model.predict_on_batch(np.array([sample.current_observation[0] for sample in batch_sample]))
        X = np.array([sample.current_observation[0] for sample in batch_sample])
        q_predicted = self.target_model.predict_on_batch(np.array([sample.new_observation[0] for sample in batch_sample]))
        for i in range(mini_batch_size):
            sample = batch_sample[i]
            if sample.done:
                y[i][sample.action] = sample.reward
            else:
                y[i][sample.action] = sample.reward + self.gamma*np.max(q_predicted[i])
        return X, y
        
    def fit(self, num_episodes=100, replay_memory_capacity=50000, num_steps_warmup=50, mini_batch_size=32, verbose=1, visualize=False, save_best=False, saved_best_performance=None):
        replay_memory = deque(maxlen=replay_memory_capacity)
        current_step = 0
        if save_best:
            if not hasattr(self.env, 'worst_performance') or not hasattr(self.env, 'best_performance') or not hasattr(self.env, 'save_name'):
                raise Exception("Env is missing an attribute for at least one of: worst_performance, best_performance, save_name")
            if saved_best_performance:
                self.best_performance = saved_best_performance
            else:
                self.best_performance = self.env.worst_performance
        for episode in range(1, num_episodes+1):
            current_observation  = self.env.reset()
            done = False
            episode_step = 0
            episode_rewards = []
            episode_max_q = []
            episode_min_q = []
            while not done:
                if self.processor:
                    processed_current_observation = self.processor.process_observation(current_observation)
                    legal_moves = self.processor.get_legal_moves(current_observation, self.env.action_space.n)
                else:
                    processed_current_observation = current_observation
                    legal_moves = np.ones(self.env.action_space.n)
                q_values = self.target_model.predict(processed_current_observation)
                action = self.policy.get_action(q_values, warm_up=current_step < num_steps_warmup, mask=legal_moves)
                if self.processor:
                    processed_action = self.processor.process_action(action)
                else:
                    processed_action = action
                new_observation, reward, done, info = self.env.step(processed_action)
                current_step += 1
                episode_step += 1
                if self.processor:
                    processed_new_observation = self.processor.process_observation(new_observation)
                else:
                    processed_new_observation = new_observation
                replay_memory.append(Transition(processed_current_observation, action, reward, processed_new_observation, done))
                current_observation = new_observation
                if visualize:
                    self.env.render()
                if current_step < num_steps_warmup:
                    continue
                else:
                    batch_sample = random.sample(replay_memory, mini_batch_size)
                    X, y = self.create_targets(batch_sample, mini_batch_size)
                    self.model.fit(X, y, batch_size=mini_batch_size, verbose=0)
                    if self.target_model_update >= 1 and current_step % self.target_model_update == 0:
                        self.update_target_model_hard()
                    
                    episode_max_q.append(np.max(q_values))
                    episode_min_q.append(np.min(q_values))
                    episode_rewards.append(reward)
            self.episode_metrics = {
                "episode" : str(episode) + "/" + str(num_episodes),
                "mean_q" : [np.mean(episode_min_q), np.mean(episode_max_q)],
                "total_reward" : np.sum(episode_rewards),
                "num_steps_in_episode" : episode_step,
                "current_step" : current_step
            }
            self.print_metrics(verbose)
            if save_best:
                if self.env.best_performance > self.best_performance:
                    self.best_performance = self.env.best_performance
                    self.save_weights('{}_dqn_weights.h5f'.format(self.env.save_name), overwrite=True)

    def save_weights(self, filepath, overwrite=True):
        self.model.save_weights(filepath, overwrite=overwrite)
        
    def load_weights(self, filepath):
        self.model.load_weights(filepath)
        self.update_target_model_hard()
    
    def print_metrics(self, verbose):
        if verbose != 0:
            print(self.episode_metrics)
        else:
            print(self.episode_metrics["episode"])
            