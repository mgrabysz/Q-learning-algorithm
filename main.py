import numpy as np
import random
import math
import time
import json
import pandas as pd

from environment import Environment


def decision(probability):
    """
    Returns True with given probability (otherwise returns False)
    """
    return random.random() < probability


def qlearn(
    env,
    agent='quber',

    num_episodes=10000,
    max_steps_per_episode=100,

    learning_rate=0.3,
    discount_rate=0.99,

    exploration_rate = 1,
    max_exploration_rate = 1,
    min_exploration_rate = 0.01,
    exploration_decay_rate = 0.0001,

    path_to_save="qlearn.json"
    ):
    """
    Main function performing Q-learning algorithm
    """

    if agent not in ['quber', 'random']:
        raise Exception("Agent can be either 'quber' or 'random'")

    success_counter = 0
    is_success_achieved = False
    episode_with_first_success = None
    action_space_size = 4
    state_space_size = env.space()

    q_table = np.zeros((state_space_size, action_space_size))
    rewards_all_episodes = []
    steps_all_episodes = []
    exploration_rates = {}  # episode : exploration rate at the end of episode

    start_time = time.time()

    for episode in range(num_episodes):
        env.reset()
        state = env.state()

        done = False
        rewards_current_episode = 0

        for step in range(max_steps_per_episode):

            available_actions = env.available_actions()

            if agent == 'quber':
                # choose action according with strategy

                if decision(exploration_rate):
                    # explore
                    action = random.choice(available_actions)

                else:
                    # exploit
                    while True:
                        action = np.argmax(q_table[state, :])
                        if action in available_actions:
                            break
                        else:
                            q_table[(state, action)] = -math.inf  # this action is not available in this state

            else:   # agent is random
                action = random.choice(available_actions)

            # end if

            new_state, reward, done = env.step(action)

            q_table[state, action] = q_table[state, action] * (1 - learning_rate) + \
                learning_rate * (reward + discount_rate * np.max(q_table[new_state, :]))

            state = new_state
            rewards_current_episode += reward

            if done:
                success_counter += int(env.get_agent_won())

                if env.get_agent_won() and not is_success_achieved:
                    episode_with_first_success = episode
                    is_success_achieved = True

                break

            exploration_rate = min_exploration_rate + \
                (max_exploration_rate - min_exploration_rate) * np.exp(-exploration_decay_rate*episode)

            # end of step

        rewards_all_episodes.append(rewards_current_episode)
        steps_all_episodes.append(step)
        exploration_rates[episode] = exploration_rate

        # end of episode

    execution_time = time.time() - start_time
    execution_time = round(execution_time, ndigits=4)

    to_save = {
        "episodes": num_episodes,
        "learn. rate": learning_rate,
        "time": execution_time,
        "final exp. rate": exploration_rate,
        "exp. decay rate": exploration_decay_rate,
        "successes": success_counter,
        "first success": episode_with_first_success
    }

    # average reward per n episodes
    rewards_per_n_episodes = np.split(np.array(rewards_all_episodes), 100)
    n = num_episodes // 100
    average_rewards = {}
    count = n

    for r in rewards_per_n_episodes:
        mean = np.mean(r)
        average_rewards[count] = mean
        count += n

    # average steps per n episodes
    steps_per_n_episods = np.split(np.array(steps_all_episodes), 100)
    n = num_episodes // 100
    average_steps = {}
    count = n

    for s in steps_per_n_episods:
        mean = np.mean(s)
        average_steps[count] = mean
        count += n

    to_save["avg reward"] = average_rewards
    to_save["avg steps"] = average_steps
    to_save["exploration rates"] = exploration_rates

    with open(path_to_save, 'w') as file_handle:
        json.dump(to_save, file_handle, indent=4)

    return q_table


def generate_path(env, q_table):
    """
    Returns a list of actions (up, down, left, right) which are
    the best according to given qtable.
    Function informational purpose

    Parameters:
    env : Environment
    q_table : np.array (2D)
    """
    done = False
    actions = []
    env.reset()
    state = env.state()

    while not done:
        action = np.argmax(q_table[state, :])

        if action == 0:
            actions.append("up")
        elif action == 1:
            actions.append("right")
        elif action == 2:
            actions.append("down")
        else:
            actions.append("left")

        state, reward, done = env.step(action)

    return actions


if __name__ == "__main__":

    file_name = "quber_1"

    size = 8
    end = (size-1, size-1)
    environment = Environment(size=size, probability = 0.4, start_point=(0,0), end_point=end, seed=1, bad_square=-30, good_square=-1, end_square=30)

    json_path = "json_files/" + file_name + ".json"
    csv_path = "csv_files/" + file_name + ".csv"

    # execute qlearn function

    q_table = qlearn(
        env=environment,
        agent='quber',

        num_episodes=10000,
        max_steps_per_episode=1000,

        learning_rate=0.3,
        discount_rate=0.99,

        exploration_rate = 1,
        max_exploration_rate = 1,
        min_exploration_rate = 0.01,
        exploration_decay_rate = 0.0001,

        path_to_save=json_path
    )

    # save q table to file
    column_names = ["up", "right", "down", "left"]
    df = pd.DataFrame(data=q_table, columns=column_names)
    df.to_csv(csv_path, index=False)
