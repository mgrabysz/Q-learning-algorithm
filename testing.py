import pandas as pd

from main import qlearn, generate_path
from environment import Environment

def automatic_testing():

    param_tested = 'squares_set'

    values_to_test = [
        (-5, -1, 5),
    ]

    for count, values in enumerate(values_to_test):

        count = 4
        file_name = param_tested + '=' + str(count)

        bad = values[0]
        good = values[1]
        end_val = values[2]

        size = 8
        end = (size-1, size-1)
        environment = Environment(size=size, probability = 0.4, start_point=(0,0), end_point=end, seed=1, bad_square=bad, good_square=good, end_square=end_val)

        json_path = "json_files/" + file_name + ".json"
        csv_path = "csv_files/" + file_name + ".csv"
        latex_name = file_name + ".latex"

        # execute qlearn function

        q_table = qlearn(
            env=environment,
            agent='quber',

            num_episodes=1000,
            max_steps_per_episode=100,

            learning_rate=0.3,
            discount_rate=0.99,

            exploration_rate = 1,
            max_exploration_rate = 1,
            min_exploration_rate = 0.01,
            exploration_decay_rate = 0.05,

            path_to_save=json_path
        )

        # save q table to file
        column_names = ["up", "right", "down", "left"]
        df = pd.DataFrame(data=q_table, columns=column_names)
        df.to_csv(csv_path, index=False)

        # moves = generate_path(environment, q_table)
        # print(moves)
        # print(len(moves))


automatic_testing()