import numpy as np

#initializing constants ---
MAX_ARROWS = 3
MAX_MATS = 2
KNIFE_DMG = 50
ARROW_DMG = 25
GAMMA = 0.999
DELTA = 0.001
#----

REWARD = np.zeros((5, 4, 3, 2, 101))
# format: IJ state, numarrows, nummats, mmstate, mhealth

TEAM_NO = 8
STEP_ERR_ARR = [0.5, 1, 2]
STEPCOST = -10 / STEP_ERR_ARR[TEAM_NO % 3]

def val_iter():

    finished = False
    DDDDD = np.zeros((5, 4, 3, 2, 101))
    while not finished:
        
        for stateVars, _ in np.ndenumerate(DDDDD):
            if stateVars[5] == 0: #MMdead
                continue
            newBest = float('-inf')




if __name__ == "__main__":
    val_iter()