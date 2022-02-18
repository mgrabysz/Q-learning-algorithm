import matplotlib.pyplot as plt
from sklearn import preprocessing
import json
import numpy as np


def load_output_from_json(path, parameter):
    with open(path, 'r') as file_handle:
        data = json.load(file_handle)
        dict = data[parameter]

        params = []
        episodes = []

        for key, value in dict.items():
            params.append(value)
            episodes.append(int(key))

        return params, episodes


def normalize_but_better(array):
    array = np.array(array)
    min = np.min(array)

    if min < 0:
        array -= min

    array = preprocessing.normalize([array], norm='max')
    return array[0]


def first_half(array):
    length = len(array)
    middle_index = length // 2
    first_half = array[:middle_index]
    return first_half


def first_quarter(array):
    half = first_half(array)
    return first_half(half)


if __name__ == '__main__':

    path = "/home/marcin/Projekty/Python/wsi/lab_6/json_files/exp_decay=0.5.json"
    # param = "avg steps"
    title = "Exp. decay = 0,5"
    xlabel = "Episodes"
    ylabel = "Normalized values"

    y1, x1 = load_output_from_json(path, "avg reward")
    y1 = normalize_but_better(y1)

    # x1 = first_quarter(x1)
    # y1 = first_quarter(y1)

    plt.plot(x1, y1, label="Average reward")

    y2, x2 = load_output_from_json(path, "avg steps")
    y2 = normalize_but_better(y2)

    # x2 = first_quarter(x2)
    # y2 = first_quarter(y2)

    plt.plot(x1, y2, label="Average step")

    y3, x3 = load_output_from_json(path, "exploration rates")
    y3 = normalize_but_better(y3)

    # x3 = first_quarter(x3)
    # y3 = first_quarter(y3)

    plt.plot(x3, y3, label="Exploration rate")

    plt.legend()

    plt.ylabel(ylabel)
    plt.xlabel(xlabel)
    plt.title(title)

    # plt.annotate('First success',
    #         xy=(6604, -32), xycoords='data',
    #         xytext=(32, 50), textcoords='offset points',
    #         arrowprops=dict(facecolor='black', shrink=0.05),
    #         horizontalalignment='right', verticalalignment='bottom')

    png_file = "pictures/" + str(title) + '.png'
    plt.savefig(png_file)
    plt.show()
    plt.clf()
