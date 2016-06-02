import unittest
from pprint import pprint
import mock
import random

class DeckEmptyException(Exception):
    pass


class Game(object):
    def __init__(self, deck, players):
        self.players = players

    def play(self):
        return self.players[0]


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

    def test_play(self):
        deck = CardDeck()
        player_1 = Player()
        game = Game(deck, [player_1])
        result = game.play()
        assert result in [ player_1, None ]

    # def test_deal(self):
    #     deck = CardDeck()
    #     player_1 = Player()
    #     game = Game(deck, [player_1])
    #     game.deal()

    def test_21_for_one_player(self):
        deck = mock.MagicMock()
        deck.draw.side_effect = [11, 10]
        player_1 = Player()
        game = Game(deck, [player_1])
        result = game.play()
        self.assertIs(result, player_1)

    @mock.mock("random.random")
    def test_21_for_second_player_always_stick(self):
        deck = mock.MagicMock()
        deck.draw.side_effect = [5, 11, 4, 10, 9]
        # TODO: Control behaviour of players to ensure the result is constant
        player_1 = Player()
        player_2 = Player()
        game = Game(deck, [player_1, player_2])
        result = game.play()
        self.assertIs(result, player_2)

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
