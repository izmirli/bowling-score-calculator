"""Bowling Score Calculator.

[TDD exercise]
Get a string of one bowling game line, and return score.
Example: '20 00 X 1/ 03 04 00 00 00 70' should return: 46

There are 10 pines you try to knock down in each frame.
A strike - knock all 10 pins with the first ball.
A spare - knock all 10 pins with the second ball (2 throws).
Each games consists of ten frames. If you bowl a strike in the tenth frame,
you get two more balls. If you throw a spare, you get one more ball.

Scoring is based on the number of pins you knock down. However, if you bowl a
spare, you get to add the pins in your next ball to that frame. For strikes,
you get the next two balls.

Line string has 10 (or 11) frames separated by a single space.
Each frame has 2 (or 1) characters - one for each throw.
The 1st can be a digit [0-9] or X to represent a strike.
The 2nd can be a digit [0-9] or / to represent a spare.

Example implementation:
https://www.sportcalculators.com/bowling-score-calculator
[no need gor GUI]
"""
import unittest
import re
import logging

logging.basicConfig(
    format='[%(asctime)s.%(msecs)03d %(levelname)s] %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO
)


def calculate_line_score(frames: list) -> int:
    """Calculate score of one bowling game line.

    :param frames: frames list of one bowling game line.
    :return: bowling game line score.
    """
    score = 0
    frame_score = build_frame_score(frames)
    logging.debug(f'frame_score: {frame_score}')

    for i in range(10):
        score += frame_score[i][1] + frame_score[i][2]
        logging.debug(f'\tFrame#{i} score(t1): {score}')

        # handle spare/strike extra score.
        next_frame = i + 1
        next_try = 1
        if frame_score[i]['add'] >= 1:
            score += frame_score[next_frame][next_try]
            logging.debug(f'\tFrame#{i} score(t2): {score}')

            if frame_score[i]['add'] == 2:
                next_try = 2
                # handle extra frame case
                if frame_score[next_frame][1] == 10:
                    next_try = 1
                    next_frame = next_frame if next_frame == 10 else next_frame + 1

                score += frame_score[next_frame][next_try]
                logging.debug(f'\tFrame#{i} score(t3): {score}')

        logging.debug(f'\tFrame#{i} score: {score}')

    return score


def build_frame_score(frames: list) -> dict:
    """Proccess frames and create enriched data structure for score calc.

    :param frames: list of frames-strings from bowling results line.
    :type frames: list
    :return: dict with frame numbers keys, values are dicts with score data.
    :rtype: dict
    """
    logging.debug(f'frames: {frames}')
    frame_score = {}
    for i, frame in enumerate(frames):
        if i == 10:
            first = 10 if frame[0] == 'X' else int(frame[0])
            frame_score[10] = {1: first, 2: 0, 'add': 0}
            if len(frame) == 2:
                if frame[1] == '/':
                    frame_score[10][2] = 10 - int(frame[0])
                else:
                    frame_score[10][2] = 10 if frame[1] == 'X' else int(frame[1])
        elif frame.upper() == 'X':
            frame_score[i] = {1: 10, 2: 0, 'add': 2}
        elif frame[-1] == '/':
            frame_score[i] = {1: int(frame[0]), 2: 10 - int(frame[0]), 'add': 1}
        else:
            frame_score[i] = {1: int(frame[0]), 2: int(frame[1]), 'add': 0}

    return frame_score


def get_bowling_line(line_str: str = '') -> list:
    """Get bowling line from user, validate format and return as frames list.

    :param line_str: bowling line string to substitute input.
    :return: list of frames strings from the line.
    """
    if line_str == '':
        line_str = input("Enter line's 10 frames: ")
    if not re.match(
            r'\s*([0-9][0-9/]|X)( ([0-9][0-9/]|X)){9}( [0-9X][0-9/X]?)?',
            line_str
    ):
        raise ValueError('Invalid line frames')

    return line_str.split()


def get_score(line_str: str) -> int:
    """Get bowling result line from input & return its score."""
    line = get_bowling_line(line_str)
    return calculate_line_score(line)


def main():
    """Get a bowling result line (game), calculate score and prit it."""
    while True:
        # '12 4/ 20 X 35 X X 9/ 4/ X 9/' => 146
        line = get_bowling_line()
        score = calculate_line_score(line)
        print(score)


class SanityTest(unittest.TestCase):
    """Test the bowling score calc code."""

    def test_lines(self):
        """Test defernt lines to be processed and their expected results."""
        cases = (
            ('00 00 00 00 00 00 00 00 00 00', 0),
            ('02 00 00 00 00 30 00 00 00 07', 12),
            ('2/ 00 00 00 00 30 00 00 00 07', 20),
            ('2/ 00 00 00 00 3/ 00 00 00 07', 27),
            ('2/ 00 00 00 00 3/ 40 00 00 07', 35),
            ('20 00 X 00 00 30 40 00 00 07', 26),
            ('20 00 X 10 00 30 40 00 00 07', 28),
            ('20 00 X 12 00 30 40 00 00 07', 32),
            ('20 X X 12 00 30 40 00 00 07', 53),
            ('20 00 X 1/ 03 04 00 00 00 70', 46),
            ('20 00 X 1/ X 04 00 00 00 70', 67),
            ('20 00 X 1/ 03 04 00 00 00 0/ 1', 50),
            ('12 4/ 20 X 35 X X 9/ 4/ X 81', 145),
            ('12 4/ 20 X 35 X X 9/ 4/ X 9/', 146)
        )
        for i, case in enumerate(cases[:14]):
            with self.subTest(f'case#{i}: {case[0]} => {case[1]}'):
                self.assertEqual(
                    get_score(case[0]), case[1], f'string: {case[0]}'
                    )
                logging.info(f'Success - case#{i}:\t{case[0]:33} => {case[1]}')

    def test_invalid(self):
        """Test invalid score line format."""
        with self.assertRaises(ValueError):
            get_score('bla')


if __name__ == '__main__':
    unittest.main()
