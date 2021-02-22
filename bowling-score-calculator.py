"""Bowling Score Calculator

Get a string of one bowling game line: 10 frames
Return score.

Example https://www.sportcalculators.com/bowling-score-calculator
[no need gor GUI]
"""
import unittest
import re
import logging

logging.basicConfig(format='%(asctime)-15s %(message)s', level=logging.DEBUG)


def calculate_line_score(frames: list) -> int:
    # logging.debug(f'frames: {frames}')
    frame_score = {}
    score = 0
    for i, frame in enumerate(frames):
        if i == 10:
            first = 10 if frame[0] == 'X' else int(frame[0])
            frame_score[10] = {1: first, 2: 0, 'add': 0}
            if len(frame) == 2:
                frame_score[10][2] = 10 if frame[1] == 'X' or frame[1] == '/' else int(frame[1])
        elif frame.upper() == 'X':
            frame_score[i] = {1: 10, 2: 0, 'add': 2}
        elif frame[-1] == '/':
            frame_score[i] = {1: int(frame[0]), 2: 10 - int(frame[0]), 'add': 1}
        else:
            frame_score[i] = {1: int(frame[0]), 2: int(frame[1]), 'add': 0}

    for i in range(10):
        score += frame_score[i][1] + frame_score[i][2]
        next_frame = i + 1
        next_try = 1
        if frame_score[i]['add'] >= 1:
            score += frame_score[next_frame][next_try]

            if frame_score[i]['add'] == 2:
                next_try = 2
                # handle two strikes case
                if frame_score[next_frame][1] == 10:
                    next_try = 1
                    next_frame = next_frame if next_frame == 10 else next_frame + 1

    return score


def get_bowling_line(line_str: str = '') -> list:
    if line_str == '':
        line_str = input("Enter line's 10 frames: ")
    if not re.match(r'\s*([0-9][0-9/]|X)( ([0-9][0-9/]|X)){9}( [0-9X][0-9/X]?)?', line_str):
        raise ValueError('Invalid line frames')

    return line_str.split()


def get_score(line_str: str) -> int:
    line = get_bowling_line(line_str)
    return calculate_line_score(line)


def main():
    while True:
        # '12 4/ 20 X 35 X X 9/ 4/ X 9/' => 146
        line = get_bowling_line()
        score = calculate_line_score(line)
        print(score)


class Sanity(unittest.TestCase):

    # def test_zero(self):
    #     self.assertEqual(0, get_score('00 00 00 00 00 00 00 00 00 00'))

    def test_lines(self):
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
        for i, case in enumerate(cases[:8]):
            with self.subTest(f'case#{i}: {case[0]} => {case[1]}'):
                self.assertEqual(get_score(case[0]), case[1], f'string: {case[0]}')
            logging.debug(f'Success - case#{i}: {case[0]} => {case[1]}')


if __name__ == '__main__':
    unittest.main()
