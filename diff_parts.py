import numpy as np
import json
import pickle
from part_2 import positionMap

reversePosMap = {
    'C':0,
    'N':1,
    'S':2,
    'E':3,
    'W':4,
    'R':1,
    'D':0
}

file1 = "a.pkl"
file2 = "outputs/part_3_output.json"

pos = [-1] * 5
for idx, i in enumerate(positionMap):
    # print(idx, i)
    pos[idx] = i.upper()

mState = ['D', 'R']

with open(file1, 'rb')as fd:
    hist1, histActions1 = pickle.load(fd)
    policy1 = np.array(histActions1[-1])

with open(file2, 'rb')as fd:
    dict = json.load(fd)
    policylist = np.array(dict['policy'])

policy2 = np.full(policy1.shape, "abhijeeth")
for i in policylist:
    # print(i)
    index = tuple([reversePosMap[i[0][0]], i[0][1], i[0][2], reversePosMap[i[0][3]], i[0][4]//25])
    policy2[index] = i[1]

for state, _ in np.ndenumerate(policy1):
    if policy1[state] != policy2[state]:
        out_state = list(state).copy()
        out_state[0] = pos[out_state[0]]
        out_state[4] *= 25
        out_state[3] = mState[out_state[3]]
        print(out_state, '\t', policy1[state], '     \t', policy2[state])
