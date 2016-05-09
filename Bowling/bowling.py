import unittest
from pprint import pprint

class Game(object):
    
    def __init__(self):
        self.balls = 0
        self.score = 0
        self.pins = []
        for _ in range(21):
            self.pins.append(0)

    def roll(self, *args):
        for pins in args:
            self.pins[self.balls] = pins
            self.balls += 1

    def getScore(self):
        self.score = 0
        ball = 0
        frame = 1
        last_frame = 10
        while frame <= last_frame:
            if self.isStrike(ball):
                self.scoreStrike(ball)
                ball += 1
            elif self.isSpare(ball):
                self.scoreSpare(ball)
                ball += 2
            else:
                self.score += self.pins[ball] + self.pins[ball + 1]
                ball += 2
            frame += 1
        return self.score

    def isSpare(self, ball):
        return self.pins[ball] + self.pins[ball + 1] == 10

    def isStrike(self, ball):
        return self.pins[ball] == 10

    def scoreSpare(self, ball):
        self.score += self.pins[ball] + self.pins[ball + 1] + self.pins[ball + 2]

    def scoreStrike(self, ball):
        self.score += self.pins[ball] + self.pins[ball + 1] + self.pins[ball + 2]

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
        self.game.roll(10, 10, 10, 10, 10, 10, 10, 10, 10)
        self.game.roll(10, 10, 10)
        self.assertEquals(self.game.getScore(), 300)

    def test_08_almost_perfect_game_240(self):
        self.game.roll(10, 10, 10, 10, 10, 10, 10, 10, 10)
        self.game.roll(0, 0)
        self.assertEquals(self.game.getScore(), 240)

    def test_09_almost_perfect_game_286(self):
        self.game.roll(10, 10, 10, 10, 10, 10, 10, 10, 10)
        self.game.roll(10, 6, 4)
        self.assertEquals(self.game.getScore(), 286)

    def test_10_almost_perfect_game_278(self):
        self.game.roll(10, 10, 10, 10, 10, 10, 10, 10, 10)
        self.game.roll(10, 2, 4)
        self.assertEquals(self.game.getScore(), 278)

    def test_11_almost_perfect_game_268(self):
        self.game.roll(10, 10, 10, 10, 10, 10, 10, 10, 10)
        self.game.roll(3, 7, 5)
        self.assertEquals(self.game.getScore(), 268)

    def test_12_almost_perfect_game_254(self):
        self.game.roll(10, 10, 10, 10, 10, 10, 10, 10, 6, 4)
        self.game.roll(3, 7, 5)
        self.assertEquals(self.game.getScore(), 254)

    def test_13_almost_perfect_game_247(self):
        self.game.roll(10, 10, 10, 10, 10, 10, 10, 10, 6, 4)
        self.game.roll(3, 5)
        self.assertEquals(self.game.getScore(), 247)

    def test_14_almost_perfect_game_276(self):
        self.game.roll(10, 10, 10, 10, 10, 10, 10, 10, 6, 4)
        self.game.roll(10, 10, 10)
        self.assertEquals(self.game.getScore(), 276)

    def test_15_mikes_googly(self):
        self.game.roll(1, 7, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0)
        self.assertEquals(self.game.getScore(), 12 )

    def test_16_uncle_bobs_golden_game(self):
        self.game.roll(1, 4, 4, 5, 6, 4, 5, 5, 10, 0, 1, 7, 3, 6, 4, 10, 2, 8, 6)
        self.assertEquals(self.game.getScore(), 133 )


if __name__ == '__main__':
    unittest.main()
