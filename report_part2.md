# Report

Team 8  - Dunder Mifflin - Abhijeeth Singam,  Saravanan Senthil

Interpretation of the trace:

- Since step-cost is -5, IJ is more tolerant to 'wasting' moves to avoid getting hit by moving to centre or east when the monster is in ready state. We see this especially in the West square when MM is ready to attack. In such a state, IJ's best action is simply to STAY until MM goes into the dormant state.
- We notice that IJ often tries to move towards east. This is because east is prime attacking location where IJ's attacks have the highest probability of success. 
- Based on the trace, we can tell that a common pattern of moves is:
  - Move to East
  - Maybe choose to gather and craft arrows depending on if MM is ready to attack
  - Hit repeatedly



Simulations:

1. Start: (W, 0, 0, D, 100)

	```
	state:  ('W', 0, 0, 'D', 100) ;action:  RIGHT
	state:  ('C', 0, 0, 'R', 100) ;action:  DOWN
	state:  ('S', 0, 0, 'R', 100) ;action:  GATHER
	state:  ('S', 0, 0, 'D', 100) ;action:  UP
	state:  ('C', 0, 0, 'D', 100) ;action:  RIGHT
	state:  ('E', 0, 0, 'D', 100) ;action:  HIT
	state:  ('E', 0, 0, 'R', 100) ;action:  HIT
	state:  ('E', 0, 0, 'D', 100) ;action:  HIT
	state:  ('E', 0, 0, 'D', 100) ;action:  HIT
	state:  ('E', 0, 0, 'R', 100) ;action:  HIT
	state:  ('E', 0, 0, 'R', 100) ;action:  HIT
	state:  ('E', 0, 0, 'R', 100) ;action:  HIT
	state:  ('E', 0, 0, 'R', 50) ;action:  HIT
	state:  ('E', 0, 0, 'D', 75) ;action:  HIT
	state:  ('E', 0, 0, 'D', 25) ;action:  HIT
	state:  ('E', 0, 0, 'D', 25) ;action:  HIT
	state:  ('E', 0, 0, 'D', 25) ;action:  HIT
	state:  ('E', 0, 0, 'D', 25) ;action:  HIT
	```

Comments:
- In step 3, we see IJ chooses to GATHER even though IJ never actually crafts and shoots. The reason for this is because GATHER acts similar to STAY but with a 100% success rate. This enables him to avoid moving to the east with a 15% chance. Avoiding this 15% chance is more important to IJ than gaining the one material.
- After that, we see IJ simply moving to east and constantly choosing to HIT. This is because the net step cost of gather enough materials, crafting them into arrows, moving to suitable position, shooting them, gathering more materials, and crafting those again and finally killing MM with the last few shots is more than the step cost of simply going to east and hitting MM repeatedly until MM dies. This is a common trend we see across many different starting states.
	

2. Start : (C, 2, 0, R, 100)

```
state:  ('C', 2, 0, 'R', 100) ;action:  UP
state:  ('N', 2, 0, 'R', 100) ;action:  CRAFT
state:  ('N', 1, 1, 'D', 100) ;action:  CRAFT
state:  ('N', 0, 3, 'R', 100) ;action:  STAY
state:  ('N', 0, 3, 'R', 100) ;action:  STAY
state:  ('N', 0, 3, 'D', 100) ;action:  DOWN
state:  ('C', 0, 3, 'D', 100) ;action:  RIGHT
state:  ('E', 0, 3, 'D', 100) ;action:  SHOOT
state:  ('E', 0, 2, 'D', 75) ;action:  SHOOT
state:  ('E', 0, 1, 'D', 50) ;action:  SHOOT
state:  ('E', 0, 0, 'D', 25) ;action:  HIT
state:  ('E', 0, 0, 'R', 25) ;action:  HIT
state:  ('E', 0, 0, 'R', 25) ;action:  HIT
state:  ('E', 0, 0, 'D', 50) ;action:  HIT
state:  ('E', 0, 0, 'D', 50) ;action:  HIT
state:  ('E', 0, 0, 'R', 50) ;action:  HIT
state:  ('E', 0, 0, 'R', 50) ;action:  HIT
state:  ('E', 0, 0, 'R', 50) ;action:  HIT
state:  ('E', 0, 0, 'R', 50) ;action:  HIT
state:  ('E', 0, 0, 'R', 50) ;action:  HIT
state:  ('E', 0, 0, 'R', 50) ;action:  HIT
state:  ('E', 0, 0, 'D', 75) ;action:  HIT
state:  ('E', 0, 0, 'D', 25) ;action:  HIT
state:  ('E', 0, 0, 'D', 25) ;action:  HIT
state:  ('E', 0, 0, 'R', 25) ;action:  HIT
state:  ('E', 0, 0, 'D', 50) ;action:  HIT

```

Comments:
- Here, in the first step we see that IJ moves UP instead of directly approaching MM and constantly performing HIT. This is because MM is in a ready state and IJ is likely to get hit. Thus, IJ moves up and avoids being hit. The reason he chooses UP instead of DOWN is due to the fact that he has 0 arrows and 2 materials. Thus by moving UP he can craft twice and gain arrows, and after 2 steps it is likely that MM has returned to the dormant state.
- We also notice that IJ continues to CRAFT even after MM enters the dormant state (the second CRAFT action). This is because IJ is already in the NORTH position and crafting would leave him with more arrows which is more useful in the long run (as we observe later). In the event that Indiana got three or maybe even 2 arrows from his first craft, he would have instead chosen to immediately move to the east square and start attacking MM with SHOOT and HIT.
- Once IJ reaches east, we see that IJ immediately shoots all three of his arrows. This is because of the chance that MM goes into the ready state and attacks IJ in which case IJ would lose all of his arrows. Thus, shooting all of them at the start is more beneficial. Also, by shooting his arrows, he reduces the number of successful HIT actions required to kill MM, and also makes the effect of getting attacked by MM less devastating (if MM has 50 health, getting HIT would mean killing MM wold require 2 successful HIT actions, while if MM has only 25 health, even after getting attacked, it would only take one successful HIT action to kill MM).
- After this, IJ continuously choose to HIT which is optimal as explained in the previous set of comments.
