import unittest
from pprint import pprint
import mock
import random

class DeckEmptyException(Exception):
    pass


class Game(object):
    def __init__(self, deck, players):
        pass


class Player(object):
    pass


class CardDeck(object):

    def __init__(self):
        self.cards = ([2, 3, 4, 5, 6, 7, 8, 9] * 4 +
                     [10] * 16 +
                     [11] * 4 )

    def draw(self):
        try:
            return self.cards.pop()
        except IndexError:
            raise DeckEmptyException

    def shuffle(self):
        random.shuffle(self.cards)

class TestGame(unittest.TestCase):

    def test_instantiation(self):
        deck = CardDeck()
        player_1 = Player()
        game = Game(deck, [player_1])


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

    def test_card_values(self):
        """
        test that we have sufficient range of card values
            4 lots of 2 thru 9 (number cards)
            4 lots of 11 (aces)
            and 16 10s (10 and picture cards)
        """
        expected = ( [ 2, 3, 4, 5, 6, 7, 8, 9 ] * 4 + 
                    [ 10 ] * 16 +
                    [ 11 ] * 4 )

        dealt = [ self.deck.draw() for _ in range (52) ]

        self.assertItemsEqual( dealt, expected )

    @mock.patch("random.shuffle")
    def test_shuffle(self, mock_shuffle):
        """
        test that the shuffle is called
        """
        self.deck.shuffle()
        mock_shuffle.assert_called_with(self.deck.cards)

if __name__ == '__main__':
    unittest.main()
