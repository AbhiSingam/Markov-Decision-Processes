import cvxpy as cp
import numpy as np
import pickle
import json
import os

TEAM_NO = 8
STEP_ERR_ARR = [0.5, 1, 2]
STEPCOST = -10 / STEP_ERR_ARR[TEAM_NO % 3]
# STEPCOST = -10


LOCATIONS = 5
MAX_MATS = 3    # This is the maximmum number of mat values (0-2)
MAX_ARROWS = 4  # This is the maximmum number of arrow values (0-3)
MON_STATES = 2
MAX_HEALTH = 5  # This is the maximmum number of monster health values (0-4) * 25
state_to_idx = np.zeros((LOCATIONS, MAX_MATS, MAX_ARROWS, MON_STATES, MAX_HEALTH))
idx_to_state = []
idx_to_state_action = []

positionMap = ['c', 'n', 's', 'e', 'w']
mstateMap = ['D', 'R']
posDic = {
    'pos': 0,
    'mat': 1,
    'arrow': 2,
    'mstate': 3,
    'mhealth': 4,
}

def validActions(state):
    '''state as input'''
    ret = []
    if state[0] == 0:
        ret = ['UP', 'LEFT', 'DOWN', 'RIGHT', 'STAY', 'SHOOT', 'HIT']
    elif state[0] == 1:
        ret = ['DOWN', 'STAY', 'CRAFT']
    elif state[0] == 2:
        ret = ['UP', 'STAY', 'GATHER']
    elif state[0] == 3:
        ret = ['LEFT', 'STAY', 'SHOOT', 'HIT']
    elif state[0] == 4:
        ret = ['RIGHT', 'STAY', 'SHOOT']

    if 'SHOOT' in ret and state[posDic['arrow']] == 0:
        ret.remove('SHOOT')
    if 'CRAFT' in ret and state[posDic['mat']] == 0:
        ret.remove('CRAFT')
    if state[posDic['mhealth']] == 0:
        ret = ['NONE']

    return ret

def get_prob(state, action):
    successState = state.copy()
    failState = state.copy()
    ret = [[0], [state.copy()]]

    if positionMap[state[0]] == 'c':
        if action in ['UP', 'STAY', 'DOWN', 'LEFT', 'RIGHT']:
            endpoint = {'UP': 1, 'STAY': 0, 'DOWN': 2, 'LEFT': 4, 'RIGHT': 3}
            successState[0] = endpoint[action]
            failState[0] = 3

            ret = [[0.85, 0.15], [successState, failState]]

        if action == 'SHOOT':
            failState[posDic['arrow']] = max(0, failState[posDic['arrow']] - 1)
            successState[posDic['arrow']] = max(
                0, successState[posDic['arrow']] - 1)
            successState[posDic['mhealth']] = max(
                0, successState[posDic['mhealth']] - 1)

            ret = [[0.5, 0.5], [successState, failState]]

        if action == 'HIT':
            successState[posDic['mhealth']] = max(
                0, successState[posDic['mhealth']] - 2)
            ret = [[0.1, 0.9], [successState, failState]]

    if positionMap[state[0]] == 'n':
        if action in ['DOWN', 'STAY']:
            endpoint = {'STAY': 1, 'DOWN': 0}
            successState[posDic['pos']] = endpoint[action]
            failState[0] = 3
            ret = [[0.85, 0.15], [successState, failState]]
        if action == 'CRAFT':
            state1 = state.copy()
            state2 = state.copy()
            state3 = state.copy()

            state1[posDic['arrow']] = min(3, state1[posDic['arrow']] + 1)
            state2[posDic['arrow']] = min(3, state1[posDic['arrow']] + 2)
            state3[posDic['arrow']] = min(3, state1[posDic['arrow']] + 3)
            state1[posDic['mat']] -= 1
            state2[posDic['mat']] -= 1
            state3[posDic['mat']] -= 1
            ret = [[0.5, 0.35, 0.15], [state1, state2, state3]]

    if positionMap[state[0]] == 's':
        if action in ['UP', 'STAY']:
            endpoint = {'STAY': 2, 'UP': 0}
            successState[posDic['pos']] = endpoint[action]
            failState[0] = 3
            ret = [[0.85, 0.15], [successState, failState]]

        if action == 'GATHER':
            successState[posDic['mat']] = min(
                2, successState[posDic['mat']] + 1)
            ret = [[0.75, 0.25], [successState, failState]]

    if positionMap[state[0]] == 'e':
        if action in ['LEFT', 'STAY']:
            endpoint = {'STAY': 3, 'LEFT': 0}
            successState[0] = endpoint[action]
            ret = [[1.0], [successState]]

        if action == 'SHOOT':
            successState[posDic['arrow']] -= 1
            failState[posDic['arrow']] -= 1
            successState[posDic['mhealth']] -= 1
            ret = [[0.9, 0.1], [successState, failState]]

        if action == 'HIT':
            successState[posDic['mhealth']] = max(
                0, successState[posDic['mhealth']] - 2)
            ret = [[0.2, 0.8], [successState, failState]]

    if positionMap[state[0]] == 'w':
        if action in ['RIGHT', 'STAY']:
            endpoint = {'STAY': 4, 'RIGHT': 0}
            successState[0] = endpoint[action]
            ret = [[1.0], [successState]]
        if action in 'SHOOT':

            successState[posDic['arrow']] -= 1
            failState[posDic['arrow']] -= 1
            successState[posDic['mhealth']] -= 1
            ret = [[0.25, 0.75], [successState, failState]]

    if action == 'NONE':
        ret = [[1], [state]]

    if(ret == [[0], [state]]):
        print("ACTION: ", action, " ", state)

    if state[posDic['mstate']] == 0:
        probs, states = ret
        temp_prob = []
        temp_state = []
        for i, val in enumerate(probs):
            temp_prob.append(val*0.8)
            temp_state.append(states[i].copy())
            rdy = states[i].copy()
            rdy[posDic['mstate']] = 1
            temp_prob.append(val*0.2)
            temp_state.append(rdy.copy())
        ret = [temp_prob, temp_state]

    else:
        probs, states = ret
        temp_prob = []
        temp_state = []
        for i, val in enumerate(probs):
            temp_prob.append(val * 0.5)
            temp_state.append(states[i].copy())

        for i, _ in enumerate(probs):
            tState = states[i].copy()
            if state[0] in [0, 3]:
                tState = state.copy()
                tState[posDic['arrow']] = 0
                tState[posDic['mhealth']] = min(
                    4, tState[posDic['mhealth']] + 1)

            tState[posDic['mstate']] = 0

            temp_prob.append(0.5 * probs[i])
            temp_state.append(tState.copy())

        ret = [temp_prob, temp_state]

    return ret

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
        modified_state[4] = modified_state[4] * 25
        modified_state[3] = mstateMap[modified_state[3]]
        policy.append([tuple(modified_state), best_action])
    return policy

def calcReward(prevState, state):
    if prevState[posDic['mstate']] == 1 and state[posDic['mstate']] == 0 and prevState[0] in [0, 3] and prevState[posDic['mhealth']] > 0:
        return -40
    # if state[4]==0 and prevState[4]>0:
    #     return 50

    return 0

def init_states():
    i = 0
    for state, _ in np.ndenumerate(state_to_idx):
        # print(state)
        state_to_idx[state] = i
        idx_to_state.append(state)
        actions = validActions(state)
        for act in actions:
            idx_to_state_action.append((state, act))
        i += 1
    # print(state_to_idx)

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
        ret[int(state_to_idx[tuple(start_state)])][0] = 1
        return ret

def solve(A, alpha, r):
    x = cp.Variable(shape=(len(idx_to_state_action), 1), name="x")
    constraints = [cp.matmul(A, x) == alpha, x >= 0]
    objective = cp.Maximize(cp.matmul(r,x))
    problem = cp.Problem(objective, constraints)

    solution = problem.solve()
    print(solution)

    # print(x.value)

    with open('lp.pkl', 'wb') as fd:
        pickle.dump(x.value, fd)
    
    x_list = []
    for i in x.value:
        x_list.append(i[0])
    
    return x, x_list, solution

if __name__ == '__main__':
    start_state = (0,0,0,0,4)
    general_case = True
    # general_case = False
    init_states()
    print(len(idx_to_state_action))

    # quit()

    A, A_list = get_A()

    with open("A_value.txt", "w") as f:
        f.write(str(A_list))

    R = get_R()
    print(A)
    alpha = get_alpha(general_case, start_state)

    alpha_list = []
    for i in alpha:
        alpha_list.append(list(i))

    x, x_list, objective = solve(A, alpha, R)
    # print(x.value)
    policy = get_policy(x)
    # print(type(list(policy)[0][0]))
    # print(type(list(x.value)[0]))

    # print(alpha)

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
