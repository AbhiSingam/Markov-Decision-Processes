import numpy as np
import json
# initializing constants ---

TEAM_NO = 8
STEP_ERR_ARR = [0.5, 1, 2]
STEPCOST = -10 / STEP_ERR_ARR[TEAM_NO % 3]

GAMMA = 0.999
DELTA = 0.001
# ----

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
    if positionMap[state[0]] == 'c':
        ret = ['UP', 'LEFT', 'DOWN', 'RIGHT', 'STAY', 'SHOOT', 'HIT', 'NONE']
    elif positionMap[state[0]] == 'n':
        ret = ['DOWN', 'STAY', 'NONE', 'CRAFT']
    elif positionMap[state[0]] == 's':
        ret = ['UP', 'STAY', 'GATHER', 'NONE']
    elif positionMap[state[0]] == 'e':
        ret = ['LEFT', 'SHOOT', 'HIT', 'NONE']
    elif positionMap[state[0]] == 'w':
        ret = ['RIGHT', 'STAY', 'SHOOT', 'NONE']

    if 'SHOOT' in ret:
        if state[posDic['arrow']] == 0:
            ret.remove('SHOOT')
    if 'CRAFT' in ret:
        if state[posDic['mat']] == 0:
            ret.remove('CRAFT')
    if state[posDic['mhealth']] == 0:
        ret = ['NONE']

    return ret

# UTILS = np.zeros((5, 4, 3, 2, 5))
# format: IJ state, numarrows, nummats, mmstate, mhealth


hist = []
hist.append(np.zeros((5, 3, 4, 2, 5)))


def get_prob(state, action):
    successState = state
    failState = state
    attackState = state
    sucRdy = state
    failRdy = state
    if positionMap[state[0]] == 'c':
        if action in ['UP', 'STAY', 'DOWN', 'LEFT', 'RIGHT']:
            endpoint = {'UP': 1, 'STAY': 0, 'DOWN': 2, 'LEFT': 4, 'RIGHT': 3}
            successState[0] = endpoint[action]
            failState[0] = 3
            
            attackState[posDic['arrow']] = 0
            attackState[posDic['mhealth']] = min(4, attackState[posDic['mhealth']] + 1)
            sucRdy = successState
            failRdy = failState
            failRdy['mstate'] = 1
            sucRdy['mstate'] = 1

            if state[posDic['mstate']] == 1: # ready
                return [0.85 * 0.5, 0.15 * 0.5, 0.5], [successState, failState, attackState]
            
            else: #dormant
                return [0.85 * 0.8, 0.15 * 0.8, 0.85 * 0.2, 0.15 * 0.2], [successState, failState, sucRdy, failRdy]

        if action == 'SHOOT':
            failState[posDic['arrow']] = max(0, failState[posDic['arrow']] - 1)
            successState[posDic['arrow']] = max(
                0, successState[posDic['arrow']] - 1)
            successState[posDic['mhealth']] = max(
                0, successState[posDic['mhealth']] - 1)
            return [0.5, 0.5], [successState, failState]

        if action == 'HIT':
            successState[posDic['mhealth']] = max(
                0, successState[posDic['mhealth']] - 2)
            return [0.1, 0.9], [successState, failState]

    if positionMap[state[0]] == 'n':
        if action in ['DOWN', 'STAY']:
            endpoint = {'STAY': 1, 'DOWN': 0}
            successState[posDic['pos']] = endpoint[action]
            failState[0] = 3
            return [0.85, 0.15], [successState, failState]
        if action == 'CRAFT':
            state1 = state
            state2 = state
            state3 = state

            state1[posDic['arrow']] = min(3, state1[posDic['arrow']] + 1)
            state2[posDic['arrow']] = min(3, state1[posDic['arrow']] + 2)
            state3[posDic['arrow']] = min(3, state1[posDic['arrow']] + 3)

            for stat in (state1, state2, state3):
                stat[posDic['mat']] -= 1

            return [0.5, 0.35, 0.15], [state1, state2, state3]

    if positionMap[state[0]] == 's':
        if action in ['UP, STAY']:
            endpoint = {'STAY': 2, 'UP': 0}
            successState[posDic['pos']] = endpoint[action]
            failState[0] = 3
            return [0.85, 0.15], [successState, failState]

        if action == 'GATHER':
            successState[posDic['mat']] = min(2, successState[posDic['mat']])
            return [0.75, 0.25], [successState, failState]

    if positionMap[state[0]] == 'e':
        if action in ['LEFT', 'STAY']:
            endpoint = {'STAY': 3, 'LEFT': 0}
            successState[0] = endpoint[action]
            return [1.0], [successState]

        if action == 'SHOOT':
            for stat in (successState, failState):
                stat[posDic['arrow']] -= 1

            successState[posDic['mhealth']] -= 1
            return [0.9, 0.1], [successState, failState]

        if action == 'HIT':
            successState[posDic['mhealth']] -= 2
            return [0.2, 0.8], [successState, failState]

    if positionMap[state[0]] == 'w':
        if action in ['RIGHT', 'STAY']:
            endpoint = {'STAY': 4, 'RIGHT': 0}
            successState[0] = endpoint[action]
            return [1.0], [successState, failState]
        if action in 'SHOOT':
            for stat in (successState, failState):
                stat[posDic['arrow']] -= 1
            successState[posDic['mhealth']] -= 1
            return [0.25, 0.75], [successState, failState]

    return [1], [state]


# def calcReward(state, prevState):
#     if state[posDic['mhealth']] == 0 and prevState[posDic['mhealth']] > 0:
#         # print('yea')
#         return 50
#     if state[posDic['mstate']] == 1 and state[0] in [0, 3] and state[posDic['mhealth']] > 0:
#         # ready
#         return -40 * 0.5

#     return 0


def calc2Prob(state):
    
    successState = state
    failState = state
    if state[posDic['mstate']] == 0:  # dormant
        successState[posDic['mstate']] = 1
        ret = 0.2 * hist[-1][successState] + 0.8 * hist[-1][failState]
    else: # ready

        successState[posDic['mstate']] = 0
        successState[posDic['mhealth']] = min(
            4, successState[posDic['mhealth']] + 1)
        successState[posDic['arrow']] = 0
        ret = 0.5 * hist[-1][successState] + 0.5*(hist[-1][failState])
        if state[0] in [1, 2, 4]:
            ret = 0
    return ret


def do_action(action, state):
    mstate = state[posDic['mstate']]
    util = 0
    probs, states = get_prob(state, action)
    for i in range(len(probs)):
        util += probs[i] * (calcReward(states[i], state) +
                            STEPCOST + GAMMA * hist[-1][states[i]])
        # util += probs[i] * (STEPCOST + GAMMA * hist[-1][states[i]] + calc2Prob(state, states[i]))
        # util += probs[i] * (STEPCOST + GAMMA * hist[-1][states[i]] + calc2Prob(state, states[i]))
        
        # p p' N, E
        # p1 p1' A NOT



    return util


def val_iter():
    finished = False
    itNum = 0
    while not finished:
        cur_utils = np.zeros(hist[0].shape)
        for state, _ in np.ndenumerate(cur_utils):
            state = list(state)
            utils_state = []
            for action in validActions(state):
                utils_state.append(do_action(action, state))
            cur_utils[state] = np.max(np.array(utils_state))
        
        hist.append(cur_utils)

        t1 = hist[-1]
        t2 = hist[-2]
        itNum += 1
        diff = np.max(np.abs(t1 - t2))
        print(itNum, diff)
        print(hist[-1][(4, 0, 3, 0, 1)])

        if diff < DELTA:
            finished = True


if __name__ == "__main__":
    initial = ('W', 0, 0, 'D', 100)
    val_iter()
    with open('thing.json', 'a+') as fd:
        json.dump(hist, fd, indent=4)
