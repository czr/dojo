import unittest
from pprint import pprint

class Game:
    def __init__(self):
        self.rolls = []
        self.roll  = 0
        for _ in range(21):
            self.rolls.append(0)
    def getScore(self):
        return 0
    def roll(self, pins):
        self.rolls[self.roll] = pins
        self.roll += 1

class TestBowlingBallKata(unittest.TestCase):
    def test_01_init(self):
        g = Game()
        self.assertEqual(len(g.rolls), 21)
    def test_02_gutter(self):
        g = Game()
        self.assertEqual(g.getScore(), 0)
    def test_03_roll_1(self):
        g = Game()
        g.roll(1)
        self.assertEqual(g.getScore(), 1)

if __name__ == '__main__':
    unittest.main()
