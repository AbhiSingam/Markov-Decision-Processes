import numpy as np
import json
import pickle
from part_2 import positionMap
import pandas as pd

dict = {
    "state":[],
    "policy1":[],
    "policy2":[],
    "policy3":[],
    "policy4": [],
}

file1 = "a.pkl"
file2 = "a1.pkl"
file3 = "a2.pkl"
file4 = "a3.pkl"

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

with open(file3, 'rb')as fd:
    hist3, histActions3 = pickle.load(fd)
    policy3 = np.array(histActions3[-1])

with open(file4, 'rb')as fd:
    hist4, histActions4 = pickle.load(fd)
    policy4 = np.array(histActions4[-1])

for state, _ in np.ndenumerate(policy1):
    if policy1[state] != policy2[state] or policy1[state] != policy3[state] or policy1[state] != policy4[state]:
        out_state = list(state).copy()
        out_state[0] = pos[out_state[0]]
        out_state[4] *= 25
        out_state[3] = mState[out_state[3]]
        dict['state'].append(out_state)
        dict['policy1'].append(policy1[state])
        dict['policy2'].append(policy2[state])
        dict['policy3'].append(policy3[state])
        dict['policy4'].append(policy4[state])
        # print(out_state, '\t', policy1[state], '     \t', policy2[state],
        #       '     \t', policy3[state], '     \t', policy4[state])

data = pd.DataFrame.from_dict(dict)
print(type(data))
data.to_markdown("table.md")