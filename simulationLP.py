import pickle
import random
import numpy as np
from part_2 import get_prob
from part_3 import idx_to_state_action, init_states

with open('lp.pkl', 'rb')as fd:
    st_act_values = pickle.load(fd)
    # print(st_act_values)


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
    best_action = 'NONE'
    best_x = np.NINF
    # print(len(idx_to_state_action))
    for idx, st_act in enumerate(idx_to_state_action):
        # print(st_act_values[idx])
        # print(best_x)
        if st_act[0] == state and st_act_values[idx] > best_x:
            best_action = st_act[1]
            best_x = st_act_values[idx]
    return best_action
            



startState = (4, 0, 2, 1, 4)
done = False
init_states()
while not done:
    best_act = get_best_action(tuple(startState))
    print('state: ', tuple(startState), ';action: ', best_act)
    startState = update_state(list(startState), best_act)

    if startState[posDic['mhealth']] == 0:
        done = True
