import pickle
import numpy as np
import os
from part_2 import positionMap
from matplotlib import pyplot as plt

with open('a2.pkl', 'rb') as fd:
    hist, actions = pickle.load(fd)

pos = [-1] * 5
for idx, i in enumerate(positionMap):
    # print(idx, i)
    pos[idx] = i.upper()

mState = ['D', 'R']

# print(pos)

#make outputdir
os.makedirs('outputs', exist_ok=True)
path = './outputs/part_2_task_2.2_trace.txt'
deltas = []


with open(path, 'w') as fd:
    for j in range(len(hist)  - 1):
        i = j+1
        t1 = hist[i]
        t2 = hist[j]
        diff = np.max(np.abs(t1 - t2))
        deltas.append(diff)
        print('iteration=' + str(j), file=fd)
        for state, _ in np.ndenumerate(hist[i]):
            # print(state)
            print('(' + pos[state[0]] + ',' + str(state[1])+ ',' + str(state[2]) + ',' + mState[state[3]] + ',' + str(state[4] * 25) + ')', end='', file=fd)
            # print(actions[i][state].astype(str))
            print(' :' + actions[i][state].astype(str) + '=[' + str(round(hist[i][state],2)) + ']', file=fd)

plt.plot(deltas, label='delta')
plt.legend()
plt.xlabel('iteration')
plt.ylabel('diff')
plt.show()
print(deltas)
