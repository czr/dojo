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

    def test_two_players_second_win(self):
        player1 = mock.MagicMock()
        player2 = mock.MagicMock()
        moves = [(player1, 10), (player2, 10), (player1, 7), (player2, 8)]
        winners = calculate_pontoon_winners(moves)
        self.assertItemsEqual(winners, [player2])

    def test_two_players_first_passed_bust_second_win(self):
        player1 = mock.MagicMock()
        player2 = mock.MagicMock()
        moves = [(player1, 10), (player2, 10), (player1, 7), (player2, 8),(player1, 5)]
        winners = calculate_pontoon_winners(moves)
        self.assertItemsEqual(winners, [player2])


def calculate_pontoon_winners(moves):
    sums = {}
    for move in moves:
        sums[move[0]] = sums.get(move[0], 0) + move[1]
    # here we have sums with all the totals per player:
    # { player1 : 17, player2: 18 }
    highest_score = max(sums.values())
    if highest_score > 21:
        return []
    winners = []
    for player in sums.keys():
        if sums[player] == highest_score:
            winners = [player]

    return winners



if __name__ == '__main__':
    unittest.main()
