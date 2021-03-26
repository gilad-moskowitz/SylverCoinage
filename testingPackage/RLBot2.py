import numpy as np
from keras.models import Sequential, Model
from keras.layers import Dense, Activation, Flatten, Input, Lambda
from keras.optimizers import Adam, RMSprop
import gym
from DQN import DQN
from DQNProcessor import CartPoleProcessor, SylverCoinageProcessor
from DQNPolicy import EpsilonGreedyPolicy
import multiprocessing
from os import path

replay_memory_capacity = 50000
epsilon = 1.0
epsilon_decay_rate = 0.9999
min_epsilon = 0.1
target_model_update = 1
gamma = 0.99
num_episodes = 10000
num_steps_warmup = 200
mini_batch_size = 64
env_name = "gym_leeav.envs:LeeavEnv-v0"



def run_bot(name="", return_dict={}):
    env = gym.make(env_name, keep_score=True, name=name)
    np.random.seed(123)
    env.seed(123)
    model = Sequential()
    model.add(Flatten(input_shape=(1,) + env.observation_space.shape))
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dense(512))
    model.add(Activation('relu'))
    model.add(Dense(256))
    model.add(Activation('relu'))
    model.add(Dense(256))
    model.add(Activation('relu'))
    model.add(Dense(256))
    model.add(Activation('relu'))
    model.add(Dense(64))
    model.add(Activation('relu'))
    model.add(Dense(64))
    model.add(Activation('relu'))
    model.add(Dense(64))
    model.add(Activation('relu'))
    model.add(Dense(env.action_space.n))
    model.add(Activation('linear'))
    model.compile(loss="mse", optimizer=RMSprop(lr=0.00025, rho=0.95, epsilon=0.01), metrics=["accuracy"])
    # model.compile(loss='mse', optimizer=Adam(lr=1e-3), metrics=['mae'])

    print(model.summary())

    policy = EpsilonGreedyPolicy(epsilon=epsilon, decay_rate=epsilon_decay_rate, min_epsilon=min_epsilon)
    processor = SylverCoinageProcessor(max_observation=100) #verify that remainingGaps also is capped
    dqn = DQN(model=model, env=env, policy=policy, processor=processor, target_model_update=target_model_update, gamma=gamma)
    # Add load and save functions
    if path.exists('best_dqn_{}_weights.h5f'.format(env_name.split(':')[-1])):
        dqn.load_weights('best_dqn_{}_weights.h5f'.format(env_name.split(':')[-1]))
    dqn.fit(num_episodes=num_episodes, num_steps_warmup=num_steps_warmup, mini_batch_size=mini_batch_size, visualize=True, save_best=True)
    win_percentage = dqn.best_performance
    return_dict[name] = win_percentage

if __name__ == "__main__":
    best_per = 0
    manager = multiprocessing.Manager()
    for j in range(1):
        return_dict = manager.dict()
        jobs = []
        updated = False
        for i in range(1):
            name = "Sylverbot" + str(i)
            p = multiprocessing.Process(target=run_bot, args=(name, return_dict))
            jobs.append(p)
            p.start()

        for proc in jobs:
            proc.join()

        
        best_file = ""
        print(return_dict)
        for file, per in return_dict.items():
            if best_per < per:
                best_file = file
                updated = True
        if updated:
            os.remove('best_dqn_{}_weights.h5f'.format(env_name.split(':')[-1]))
            os.rename("{}_dqn_weights.h5f".format(best_file), 'best_dqn_{}_weights.h5f'.format(ENV_NAME.split(':')[-1]))
    print(best_per)