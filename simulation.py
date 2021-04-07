import pickle
import random
import numpy
from part_2 import get_prob

with open('a.pkl', 'rb')as fd:
    hist, histActions = pickle.load(fd)

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


startState = (4, 0, 2, 1, 4)
done = False
while not done:
    print('state: ', tuple(startState), ';action: ', thisAction[tuple(startState)])
    startState = update_state(list(startState), thisAction[tuple(startState)])

    if startState[posDic['mhealth']] == 0:
        done = True
