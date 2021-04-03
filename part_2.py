import numpy as np

MM_health = 100
MM_state = 'D'
arrows = 3
materials = 0
position = 'C'
bladeDMG = 50
arrowDMG = 25

team = 8
step_arr = [0.5, 1, 2]
StepCost = -10/step_arr[team%3]
gamma = 0.999
delta = 0.001


# C - MovProb = 85% ShootProb = 0.5 BladeProb = 0.1
# N - MovProb = 85% 1Arrow = 0.5 2Arrow = 0.35 3Arrow = 0.15
# E - MovProb = 100% ShootProb = 0.5 BladeProb = 0.1
# W - MovProb = 100% ShootProb = 0.5 BladeProb = 0.1
# S - MovProb = 85% MatProb = 0.75
