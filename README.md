# Bowling Score Calculator

Done as part of a TDD exercise.

### Objective
Get a string of one bowling game line, and return score.

Example: `'20 00 X 1/ 03 04 00 00 00 70'` should return: 46

### Rules
There are 10 pines you try to knock down in each frame.
A strike - knock all 10 pins with the first ball.
A spare - knock all 10 pins with the second ball (2 throws).
Each games consists of ten frames. If you bowl a strike in the tenth frame,
you get two more balls. If you throw a spare, you get one more ball.

### Score
Scoring is based on the number of pins you knock down. However, if you bowl a
spare, you get to add the pins in your next ball to that frame. For strikes,
you get the next two balls.

### Input
* Line string has 10 (or 11) frames separated by a single space.
* Each frame has 2 (or 1) characters - one for each throw.
* The 1st can be a digit `0-9` or `X` to represent a strike.
* The 2nd can be a digit `0-9` or `/` to represent a spare.

#### Examples: 
* `02 00 00 00 00 30 00 00 00 07` (Score: 12)
* `20 00 X 1/ 03 04 00 00 00 70` (Score: 46)
* `20 00 X 1/ 03 04 00 00 00 0/ 1` (Score: 50)
* `12 4/ 20 X 35 X X 9/ 4/ X 81` (Score: 145)

Example implementation:
 https://www.sportcalculators.com/bowling-score-calculator
(no need for this GUI).
