import pickle
import random
import numpy
from part_2 import get_prob, positionMap

with open('a3.pkl', 'rb')as fd:
    hist, histActions = pickle.load(fd)


pos = [-1] * 5
for idx, i in enumerate(positionMap):
    # print(idx, i)
    pos[idx] = i.upper()

mState = ['D', 'R']

utils = hist[-1]
thisAction = histActions[-1]

positionMap = ['c', 'n', 's', 'e', 'w']
posDic = {
    'pos': 0,
    'mat': 1,
    'arrow': 2,
    'mstate': 3,
    'mhealth': 4,
}

def update_state(state, action2):
    # print(type(action2[0]))
    # print(action2[0][0])
    prob, states = get_prob(state, action2)
    rand = random.random()
    for i in range(len(prob) - 1):
        prob[i + 1] += prob[i]
        
    for i, pro in enumerate(prob):
        if rand <= pro:
            return states[i] 

# 1.(W, 0, 0, D, 100) 2.(C, 2, 0, R, 100)
startState = (2, 2, 1, 0, 4)
# startState = (0, 2, 0, 1, 4)
done = False
while not done:
    printState = list(startState)
    printState[0] = pos[printState[0]]
    printState[3] = mState[printState[3]]
    printState[4] *= 25
    print('state: ', tuple(printState), ';action: ', thisAction[tuple(startState)])
    startState = update_state(list(startState), thisAction[tuple(startState)])

    if startState[posDic['mhealth']] == 0:
        done = True
