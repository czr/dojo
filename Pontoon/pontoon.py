import unittest
from pprint import pprint


class DeckEmptyException(Exception):
    pass


class Game(object):
    pass


class CardDeck(object):

    def __init__(self):
        self.deck = [1] * 52

    def draw(self):
        try:
            return self.deck.pop()
        except IndexError:
            raise DeckEmptyException


class TestGame(unittest.TestCase):

    def setUp(self):
        self.game = Game()

    def tearDown(self):
        del self.game

    def test_01(self):
        pass


class TestCardDeck(unittest.TestCase):

    def setUp(self):
        self.deck = CardDeck()

    def tearDown(self):
        del self.deck

    def test_52_cards(self):
        for _ in range(52):
            card = self.deck.draw()

        with self.assertRaises(DeckEmptyException):
            self.deck.draw()


if __name__ == '__main__':
    unittest.main()
