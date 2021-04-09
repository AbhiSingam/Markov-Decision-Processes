import numpy as np
import json
import pickle
from part_2 import positionMap

file1 = "a.pkl"
file2 = "a1.pkl"

pos = [-1] * 5
for idx, i in enumerate(positionMap):
    # print(idx, i)
    pos[idx] = i.upper()

mState = ['D', 'R']

with open(file1, 'rb')as fd:
    hist1, histActions1 = pickle.load(fd)
    policy1 = np.array(histActions1[-1])

with open(file2, 'rb')as fd:
    hist2, histActions2 = pickle.load(fd)
    policy2 = np.array(histActions2[-1])

for state, _ in np.ndenumerate(policy1):
    if policy1[state] != policy2[state]:
        out_state = list(state).copy()
        out_state[0] = pos[out_state[0]]
        out_state[4] *= 25
        out_state[3] = mState[out_state[3]]
        print(out_state, '\t', policy1[state], '     \t', policy2[state])
