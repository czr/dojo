import mock
import unittest


class GameHistoryTest(unittest.TestCase):

    def test_one_player(self):
        player = mock.MagicMock()
        moves = [(player, 10), (player, 11)]
        winners = calculate_pontoon_winners(moves)
        self.assertItemsEqual(winners, [player])

    def test_one_player_bust(self):
        player = mock.MagicMock()
        moves = [(player, 10), (player, 11), (player, 2)]
        winners = calculate_pontoon_winners(moves)
        self.assertItemsEqual(winners, [])


def calculate_pontoon_winners(moves):
    return [moves[0][0]]


if __name__ == '__main__':
    unittest.main()
