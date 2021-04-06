import numpy as np
import json
import pickle

# initializing constants ---

TEAM_NO = 8
STEP_ERR_ARR = [0.5, 1, 2]
STEPCOST = -10 / STEP_ERR_ARR[TEAM_NO % 3]
# STEPCOST = -10

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
    if state[0] == 0:
        ret = ['UP', 'LEFT', 'DOWN', 'RIGHT', 'STAY', 'SHOOT', 'HIT', 'NONE']
    elif state[0] == 1:
        ret = ['DOWN', 'STAY', 'NONE', 'CRAFT']
    elif state[0] == 2:
        ret = ['UP', 'STAY', 'GATHER', 'NONE']
    elif state[0] == 3:
        ret = ['LEFT', 'SHOOT', 'HIT', 'NONE']
    elif state[0] == 4:
        ret = ['RIGHT', 'STAY', 'SHOOT', 'NONE']

    if 'SHOOT' in ret:
        if state[posDic['arrow']] == 0:
            ret.remove('SHOOT')
    if 'CRAFT' in ret:
        if state[posDic['mat']] == 0:
            ret.remove('CRAFT')
    if state[posDic['mhealth']] == 0:
        ret = ['NONE']

    if state[posDic['mhealth']] > 0 and 'NONE' in ret:
        ret.remove('NONE')

    return ret

# UTILS = np.zeros((5, 4, 3, 2, 5))
# format: IJ state, numarrows, nummats, mmstate, mhealth


hist = []
hist.append(np.zeros((5, 3, 4, 2, 5)))

cur_policy = []
cur_policy.append(np.zeros((5, 3, 4, 2, 5)))


def get_prob(state, action):
    # print(type(state))
    successState = state.copy()
    failState = state.copy()
    attackState = state.copy()
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
        # print("SOUTH_ACTION: ", action)
        if action in ['UP', 'STAY']:
            # print("SOUTH_ACTION2: ", action)
            endpoint = {'STAY': 2, 'UP': 0}
            successState[posDic['pos']] = endpoint[action]
            failState[0] = 3
            ret = [[0.85, 0.15], [successState, failState]]

        if action == 'GATHER':
            successState[posDic['mat']] = min(2, successState[posDic['mat']] + 1)
            ret = [[0.75, 0.25], [successState, failState]]

    if positionMap[state[0]] == 'e':
        if action in ['LEFT', 'STAY']:
            endpoint = {'STAY': 3, 'LEFT': 4}
            successState[0] = endpoint[action]
            ret = [[1.0], [successState]]

        if action == 'SHOOT':
            for stat in (successState, failState):
                stat[posDic['arrow']] -= 1

            successState[posDic['mhealth']] -= 1
            ret = [[0.9, 0.1], [successState, failState]]

        if action == 'HIT':
            successState[posDic['mhealth']] -= 2
            ret = [[0.2, 0.8], [successState, failState]]

    if positionMap[state[0]] == 'w':
        if action in ['RIGHT', 'STAY']:
            endpoint = {'STAY': 4, 'RIGHT': 0}
            successState[0] = endpoint[action]
            ret = [[1.0], [successState]]
        if action in 'SHOOT':
            # print(state[posDic['arrow']])
            # for stat in (successState, failState):
            #     stat[posDic['arrow']] -= 1

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
            temp_state.append(rdy)
        ret = [temp_prob, temp_state]

    else:
        # probs, states = ret
        # temp_prob = []
        # temp_state = []
        # for i, val in enumerate(probs):
        #     temp_prob.append(val * 0.5)
        #     temp_state.append(states[i])

        # attackState[posDic['mstate']] = 0
        # if state[0] in [0, 3]:
        #     attackState[posDic['arrow']] = 0
        #     attackState[posDic['mhealth']] = min(
        #         4, attackState[posDic['mhealth']] + 1)
        # temp_prob.append(0.5)
        # temp_state.append(attackState)
        # ret = [temp_prob, temp_state]
        probs, states = ret
        temp_prob = []
        temp_state = []
        for i, val in enumerate(probs):
            temp_prob.append(val * 0.5)
            temp_state.append(states[i].copy())

        # attackState[posDic['mstate']] = 0
            # attackState[posDic['arrow']] = 0

        for i, _ in enumerate(probs):
            tState = states[i].copy()
            if tState[0] in [0, 3]:
                tState = state.copy()
                tState[posDic['arrow']] = 0
                tState[posDic['mhealth']] = min(4, tState[posDic['mhealth']] + 1)

            tState[posDic['mstate']] = 0

            temp_prob.append(0.5 * probs[i])
            temp_state.append(tState)

        ret = [temp_prob, temp_state]

    return ret


def calcReward(state, prevState):
    if state[posDic['mhealth']] == 0 and prevState[posDic['mhealth']] > 0:
        # print('yea')
        return 50
    if prevState[posDic['mstate']] == 1 and state[posDic['mstate']] == 0 and state[0] in [0, 3] and state[posDic['mhealth']] > 0:
        # ready
        return -40

    return 0


def do_action(action, state):
    mstate = state[posDic['mstate']]
    util = 0
    probs, states = get_prob(state, action)
    # print('action: ', action)
    # print("PROBS AND STATES: ", probs, states)
    if action != 'NONE':
        for i in range(len(probs)):
            util += probs[i] * (calcReward(states[i], state) +
                                STEPCOST + GAMMA * hist[-1][tuple(states[i])])
            # print(hist[-1][tuple(states[i])])

    else:
        util = hist[-1][tuple(state)]

    return util


def val_iter():
    finished = False
    itNum = 0
    while not finished:
        cur_utils = np.zeros(hist[0].shape)
        cur_actions = np.full(hist[0].shape, 'ahahaa')
        for state, _ in np.ndenumerate(cur_utils):
            state = list(state)
            utils_state = []
            actionsPos = []
            for action in validActions(state):
                utils_state.append(do_action(action, state))
                actionsPos.append(action)
                # print(actionsPos)

            # print(utils_state)
            sorted_inds = np.argsort(np.array(utils_state))
            # print(sorted_inds)
            bestInd = sorted_inds[-1]
            # print(bestInd)
            cur_utils[tuple(state)] = np.max(np.array(utils_state))
            # print(type(bestInd))
            cur_actions[tuple(state)] = actionsPos[bestInd]
            # print(actionsPos[bestInd])
            
        print(cur_actions[(0, 2, 2, 1, 1)])
        print(cur_actions[(1, 2, 2, 1, 1)])
        print(cur_actions[(2, 2, 2, 1, 1)])
        print(cur_actions[(3, 2, 2, 1, 1)])
        print(cur_actions[(4, 2, 2, 1, 1)])
        hist.append(cur_utils)
        cur_policy.append(cur_actions)

        t1 = hist[-1]
        t2 = hist[-2]
        itNum += 1
        diff = np.max(np.abs(t1 - t2))
        print(itNum, diff)
        print('c: ', cur_policy[-1][(0, 2, 2, 1, 1)], hist[-1][(0, 2, 2, 1, 1)])
        print('n: ', cur_policy[-1][(1, 2, 2, 1, 1)], hist[-1][(1, 2, 2, 1, 1)])
        print('s: ', cur_policy[-1][(2, 2, 2, 1, 1)], hist[-1][(2, 2, 2, 1, 1)])
        print('e: ', cur_policy[-1][(3, 2, 2, 1, 1)], hist[-1][(3, 2, 2, 1, 1)])
        print('w: ', cur_policy[-1][(4, 2, 2, 1, 1)], hist[-1][(4, 2, 2, 1, 1)])
        if diff < DELTA:
            finished = True


if __name__ == "__main__":
    initial = ('W', 0, 0, 'D', 100)
    val_iter()
    with open('a.pkl', 'wb') as fd:
        pickle.dump((hist, cur_policy), fd)
    # with open('thing.json', 'a+') as fd:
    #     json.dump(hist, fd, indent=4)
