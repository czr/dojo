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

    def test_two_players_first_win(self):
        player1 = mock.MagicMock()
        player2 = mock.MagicMock()
        moves = [(player1, 10), (player2, 10), (player1, 8), (player2, 7)]
        winners = calculate_pontoon_winners(moves)
        self.assertItemsEqual(winners, [player1])

    def test_two_players_first_passed_bust_second_win(self):
        player1 = mock.MagicMock()
        player2 = mock.MagicMock()
        moves = [(player1, 10), (player2, 10), (player1, 7), (player2, 8), (player1, 5)]
        winners = calculate_pontoon_winners(moves)
        self.assertItemsEqual(winners, [player2])

    def test_two_players_with_same_score(self):
        player1 = mock.MagicMock()
        player2 = mock.MagicMock()
        moves = [(player1, 10), (player2, 10), (player1, 7), (player2, 7)]
        winners = calculate_pontoon_winners(moves)
        self.assertItemsEqual(winners, [player2, player1])

    def test_three_players_one_winner_one_bust(self):
        player1 = mock.MagicMock()
        player2 = mock.MagicMock()
        player3 = mock.MagicMock()
        moves = [(player1, 10), (player2, 4), (player3, 10),
                 (player1, 10), (player2, 5), (player3,  5),
                 (player1,  2), (player2, 9)]
        winners = calculate_pontoon_winners(moves)
        self.assertItemsEqual(winners, [player2])

    def test_player_first_move(self):
        player1 = mock.MagicMock()
        old_moves = []
        deck = [2, 4]
        # player_wants_to_twist will not be consulted because the player
        # has scored less than 15 points
        new_moves = calculate_move(deck, old_moves, player1, lambda:False)
        self.assertEqual(new_moves, [(player1, 2)])
        self.assertItemsEqual(deck, [4])
        self.assertItemsEqual(old_moves, [])

    def test_player_will_stick(self):
        player1 = mock.MagicMock()
        old_moves = [(player1, 10), (player1, 8)]
        deck = [2, 4]
        new_moves = calculate_move(deck, old_moves, player1, lambda:False)
        self.assertEqual(new_moves, old_moves)
        self.assertItemsEqual(deck, [2, 4])
        self.assertItemsEqual(old_moves, [(player1, 10), (player1, 8)])

    def test_player_will_twist(self):
        player1 = mock.MagicMock()
        old_moves = [(player1, 10), (player1, 8)]
        deck = [2, 4]
        new_moves = calculate_move(deck, old_moves, player1, lambda:True)
        self.assertEqual(new_moves, [(player1, 10), (player1, 8), (player1, 2)])
        self.assertItemsEqual(deck, [4])
        self.assertItemsEqual(old_moves, [(player1, 10), (player1, 8)])

    def test_player_cant_move_if_bust(self):
        self.fail("boom")

def calculate_move(deck, moves, player, player_wants_to_twist):
    score = sum( value for (p, value) in moves if p == player )
    new_moves = moves[:]
    if score < 15 or player_wants_to_twist():
        card = deck.pop(0)
        new_moves.append((player, card))
    return new_moves

def calculate_pontoon_winners(moves):
    sums = {}
    for move in moves:
        sums[move[0]] = sums.get(move[0], 0) + move[1]
    # here we have sums with all the totals per player:
    # { player1 : 17, player2: 18 }
    highest_score = 0
    winners = []
    for player in sums.keys():
        if sums[player] <= 21:
            if sums[player] > highest_score:
                winners = [player]
                highest_score = sums[player]
            elif sums[player] == highest_score:
                winners.append(player)
    return winners

if __name__ == '__main__':
    unittest.main()
