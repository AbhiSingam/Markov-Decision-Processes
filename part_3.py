import cvxpy as cp
import numpy as np
import pickle
import json
import os
from part_2 import get_prob, validActions, STEPCOST, posDic, positionMap, mstateMap
# x = cp.Variable(shape=(2, 1), name="x")
# A = np.array([[4, 3], [-3, 4]])
LOCATIONS = 5
MAX_MATS = 3    # This is the maximmum number of mat values (0-2)
MAX_ARROWS = 4  # This is the maximmum number of arrow values (0-3)
MON_STATES = 2
MAX_HEALTH = 5  # This is the maximmum number of monster health values (0-4) * 25
state_to_idx = np.zeros((LOCATIONS, MAX_MATS, MAX_ARROWS, MON_STATES, MAX_HEALTH))
idx_to_state = []
idx_to_state_action = []

def get_policy(x):
    policy = []
    for state, _ in np.ndenumerate(state_to_idx):
        best_action = 'NONE'
        best_x = np.NINF
        # print(len(idx_to_state_action))
        for idx, st_act in enumerate(idx_to_state_action):
            if st_act[0] == state and x.value[idx][0] > best_x:
                best_action = st_act[1]
                best_x = x.value[idx][0]
        # return best_action
        modified_state = list(state).copy()
        modified_state[0] = positionMap[modified_state[0]].upper()
        modified_state[4] = modified_state[4] * 4
        modified_state[3] = mstateMap[modified_state[3]]
        policy.append([tuple(modified_state), best_action])
    return policy

def calcReward(state, prevState):
    if prevState[posDic['mstate']] == 1 and state[posDic['mstate']] == 0 and state[0] in [0, 3] and state[posDic['mhealth']] > 0:
        # ready
        return -40

    return 0

def init_states():
    i = 0
    for state, _ in np.ndenumerate(state_to_idx):
        state_to_idx[state] = i
        idx_to_state.append(state)
        actions = validActions(state)
        for act in actions:
            idx_to_state_action.append((state, act))
        i += 1

def get_A():
    A = np.zeros((len(idx_to_state),len(idx_to_state_action)))
    A_list = []
    for idx, st_act in enumerate(idx_to_state_action):
        if st_act[1] == 'NONE':
            A[int(state_to_idx[st_act[0]])][idx] = 1
        else:
            probs, states = get_prob(list(st_act[0]), st_act[1])
            for i, prob in enumerate(probs):
                A[int(state_to_idx[st_act[0]])][idx] += prob
                A[int(state_to_idx[tuple(states[i])])][idx] -= prob
    for i in A:
        A_list.append(list(i))
    return A, A_list

def get_R():
    R = np.zeros(len(idx_to_state_action))
    for idx, st_act in enumerate(idx_to_state_action):
        if st_act[1] != 'NONE':
            probs, states = get_prob(list(st_act[0]), st_act[1])
            for i, prob in enumerate(probs):
                R[idx] += prob * (calcReward(st_act[0], states[i]) + STEPCOST)
    return R

def get_alpha(general_case, start_state):
    if general_case:
        return np.full((len(idx_to_state),1), 1/600)
    else:
        ret = np.zeros((len(idx_to_state),1))
        ret[state_to_idx[start_state]][0] = 1
        return ret

def solve(A, alpha, r):
    x = cp.Variable(shape=(len(idx_to_state_action), 1), name="x")
    constraints = [cp.matmul(A, x) == alpha, x >= 0]
    objective = cp.Maximize(cp.matmul(r,x))
    problem = cp.Problem(objective, constraints)

    solution = problem.solve()
    # print(solution)

    # print(x.value)

    with open('lp.pkl', 'wb') as fd:
        pickle.dump(x.value, fd)
    
    x_list = []
    for i in x.value:
        x_list.append(i[0])
    
    return x, x_list, solution

if __name__ == '__main__':
    start_state = (0,0,0,0,100)
    general_case = True
    init_states()
    print(len(idx_to_state_action))
    A, A_list = get_A()
    R = get_R()
    alpha = get_alpha(general_case, start_state)

    alpha_list = []
    for i in alpha:
        alpha_list.append(list(i))

    x, x_list, objective = solve(A, alpha, R)
    # print(x.value)
    policy = get_policy(x)
    # print(type(list(policy)[0][0]))
    # print(type(list(x.value)[0]))
    to_jsonify = {
        "a" : A_list,
        "r" : list(R),
        "alpha" : alpha_list,
        "x" : x_list,
        "policy" : list(policy),
        "objective" : float(objective)
    }

    os.makedirs("outputs", exist_ok = True)

    with open("outputs/part_3_output.json", "w") as f:
        json.dump(to_jsonify, f)
    # x = cp.Variable(shape=(len(idx_to_state_action), 1), name="x")
    # cp.matmul(A,x)
    # print(idx_to_state_action)
    # print(STEPCOST)
