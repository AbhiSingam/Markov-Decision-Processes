# Report

Team 8  - Dunder Mifflin - Abhijeeth Singam,  Saravanan Senthil

Interpretation of the trace:

- Since step-cost is -5, IJ is more tolerant to 'wasting' moves to avoid getting hit by moving to center or east when the monster is in ready state.
- Since IJ's accuracy while hitting is very low, he will often cho





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



