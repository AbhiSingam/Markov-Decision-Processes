import json
import random
import numpy as np
from part_3 import idx_to_state_action, init_states, get_prob

with open('outputs/part_3_output.json', 'rb')as fd:
    dict = json.load(fd)
    # print(st_act_values)
    policy = dict["policy"]


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

def get_best_action(state):
    reversePosMap = {
        'C': 0,
        'N': 1,
        'S': 2,
        'E': 3,
        'W': 4,
        'R': 1,
        'D': 0
    }
    for i in policy:
        tstate = i[0].copy()
        tstate[0] = reversePosMap[tstate[0]]
        tstate[3] = reversePosMap[tstate[3]]
        tstate[4] = tstate[4]//25
        if list(tstate) == list(state):
            return i[1]       
        
            



startState = (0, 0, 0, 1, 3)
# startState = start_state
done = False
init_states()
while not done:
    best_act = get_best_action(tuple(startState))
    print('state: ', tuple(startState), ';action: ', best_act)
    startState = update_state(list(startState), best_act)

    if startState[posDic['mhealth']] == 0:
        done = True
