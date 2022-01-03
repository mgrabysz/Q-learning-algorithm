import numpy as np
import random
import math
import time
from classes import Environment

def choose_action(available_actions, q_table_row):
    while True:
        a = max(q_table_row)
        actions = [i for i, j in enumerate(q_table_row) if j == a]    # indexes of all max elemenets
        action = random.choice(actions)
        if action not in available_actions:
            q_table_row[action] = - math.inf
        else:
            break

size = 8
end = (size-1, size-1)
env = Environment(size=size, probability = 0.4, start_point=(0,0), end_point=end, seed=1, bad_square=-30, good_square=-1, end_square=30)
print(env)

success_counter = 0
stop_counter = 0

action_space_size = 4
state_space_size = env.space()

q_table = np.zeros((state_space_size, action_space_size))

num_episodes = 100000
max_steps_per_episode = 1000

learning_rate = 0.3
discount_rate = 0.99

exploration_rate = 1
max_exploration_rate = 1
min_exploration_rate = 0.01
exploration_decay_rate = 0.0001

rewards_all_episodes = []

start_time = time.time()

for episode in range(num_episodes):
    env.reset()
    state = env.state()

    done = False
    rewards_current_episode = 0

    for step in range(max_steps_per_episode):

        available_actions = env.available_actions()
        exploration_rate_threshold = random.uniform(0, 1)
        if exploration_rate_threshold > exploration_rate:
            # exploit
            while True:
                action = np.argmax(q_table[state, :])
                if action in available_actions:
                    break
                else:
                    q_table[(state, action)] = -math.inf  # this action is not available in this state

        else:
            # explore
            action = random.choice(available_actions)

        new_state, reward, done = env.step(action)

        q_table[state, action] = q_table[state, action] * (1 - learning_rate) + \
            learning_rate * (reward + discount_rate * np.max(q_table[new_state, :]))

        state = new_state
        rewards_current_episode += reward

        if done:
            stop_counter += 1
            success_counter += int(env.get_agent_won())
            if success_counter == 1:
                print("First success in ", success_counter, " episode!")
            break

        exploration_rate = min_exploration_rate + \
            (max_exploration_rate - min_exploration_rate) * np.exp(-exploration_decay_rate*episode)

    rewards_all_episodes.append(rewards_current_episode)

execution_time = time.time() - start_time
execution_time = round(execution_time, ndigits=4)

to_save = {
    "episodes": num_episodes,
    "learn. rate": learning_rate,
    "time": execution_time,
    "final exp. rate": exploration_rate,
    "successes": success_counter,
    "stopped": stop_counter
}

rewards_per_thousand_episodes = np.split(np.array(rewards_all_episodes), num_episodes/1000)
count = 1000
print("Average reward per thousand episodes\n")
for r in rewards_per_thousand_episodes:
    print(count, ": ", str(sum(r/1000)))
    count += 1000

print("Q-table\n")
print(q_table)

print(to_save)
