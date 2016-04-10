import unittest
from pprint import pprint

class Game:
    
    def __init__(self):
        self.balls = 0
        self.pins = []
        for _ in range(21):
            self.pins.append(0)

    def roll(self, *args):
        for pins in args:
            self.pins[self.balls] = pins
            self.balls += 1

    def getScore(self):
        score = 0
        ball = 0
        while ball < self.balls:
            if self.isStrike(ball):
                score += self.scoreStrike(ball)
                ball += 1
            elif self.isSpare(ball):
                score += self.scoreSpare(ball)
                ball += 2
            else:
                score += self.pins[ball]
                ball += 1
        return score

    def isSpare(self, ball):
        return self.pins[ball] + self.pins[ball + 1] == 10

    def isStrike(self, ball):
        return self.pins[ball] == 10

    def scoreSpare(self, ball):
        return 10 + self.pins[ball + 2]

    def scoreStrike(self, ball):
        return 10 + self.pins[ball + 1] + self.pins[ball + 2]

class TestBowlingBallKata(unittest.TestCase):

    def setUp(self):
        self.game = Game()

    def tearDown(self):
        del self.game

    def test_00_gutter_game(self):
        self.game.roll(0)
        self.assertEquals(self.game.getScore(), 0)

    def test_01_one_scores_one(self):
        self.game.roll(1)
        self.assertEquals(self.game.getScore(), 1)

    def test_02_one_and_two_scores_three(self):
        self.game.roll(1, 2)
        self.assertEquals(self.game.getScore(), 3)

    def test_03_spare_scores_ten(self):
        self.game.roll(5, 5)
        self.assertEquals(self.game.getScore(), 10)

    def test_04_spare_and_one_scores_twelve(self):
        self.game.roll(5, 5, 1)
        self.assertEquals(self.game.getScore(), 12)

    def test_05_strike_scores_ten(self):
        self.game.roll(10)
        self.assertEquals(self.game.getScore(), 10)

    def test_06_strike_and_one_and_six_scores_twenty_four(self):
        self.game.roll(10, 1, 6)
        self.assertEquals(self.game.getScore(), 24)

    def test_07_perfect_game(self):
        self.game.roll(10, 10, 10, 10, 10, 10, 10, 10, 10, 10, 10)
        self.assertEquals(self.game.getScore(), 300)


if __name__ == '__main__':
    unittest.main()
