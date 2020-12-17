import numpy as np


def each_priority_number(data_list):
    P = {'P1': 0, 'P2': 0, 'P3': 0, 'P4': 0, 'P5': 0}
    for data in data_list:
        P[data['Priority']] += 1
    return P

weights = np.array([0.04622152766220378, 0.11360830658093238, 0.19116091751739267, 0.020011370052701493, 0.0652514149177372])\
    ** (1/2)
weights = weights / sum(weights)