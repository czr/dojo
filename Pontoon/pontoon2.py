import mock
import unittest


class GameStateTest(unittest.TestCase):

    def test_one_player(self):
        player = mock.MagicMock()
        game_state = GameState([(player, 10), (player, 11)])
        winners = calculate_pontoon_winners(game_state)
        self.assertItemsEqual(winners, [player])

    def test_one_player_stuck(self):
        player = mock.MagicMock()
        game_state = GameState([(player, 10), (player, 8), (player, None)])
        winners = calculate_pontoon_winners(game_state)
        self.assertItemsEqual(winners, [player])


    def test_one_player_bust(self):
        player = mock.MagicMock()
        game_state = GameState([(player, 10), (player, 11), (player, 2)])
        winners = calculate_pontoon_winners(game_state)
        self.assertItemsEqual(winners, [])

    def test_two_players_second_win(self):
        player1 = mock.MagicMock()
        player2 = mock.MagicMock()
        game_state = GameState([(player1, 10), (player2, 10), (player1, 7), (player2, 8)])
        winners = calculate_pontoon_winners(game_state)
        self.assertItemsEqual(winners, [player2])

    def test_two_players_first_win(self):
        player1 = mock.MagicMock()
        player2 = mock.MagicMock()
        game_state = GameState([(player1, 10), (player2, 10), (player1, 8), (player2, 7)])
        winners = calculate_pontoon_winners(game_state)
        self.assertItemsEqual(winners, [player1])

    def test_two_players_first_passed_bust_second_win(self):
        player1 = mock.MagicMock()
        player2 = mock.MagicMock()
        game_state = GameState([(player1, 10), (player2, 10), (player1, 7), (player2, 8), (player1, 5)])
        winners = calculate_pontoon_winners(game_state)
        self.assertItemsEqual(winners, [player2])

    def test_two_players_with_same_score(self):
        player1 = mock.MagicMock()
        player2 = mock.MagicMock()
        game_state = GameState([(player1, 10), (player2, 10), (player1, 7), (player2, 7)])
        winners = calculate_pontoon_winners(game_state)
        self.assertItemsEqual(winners, [player2, player1])

    def test_three_players_one_winner_one_bust(self):
        player1 = mock.MagicMock()
        player2 = mock.MagicMock()
        player3 = mock.MagicMock()
        game_state = GameState([
            (player1, 10), (player2, 4), (player3, 10),
            (player1, 10), (player2, 5), (player3,  5),
            (player1,  2), (player2, 9)
        ])
        winners = calculate_pontoon_winners(game_state)
        self.assertItemsEqual(winners, [player2])

    def test_player_first_move(self):
        player1 = mock.MagicMock()
        game_state = GameState()
        deck = [2, 4]
        # player_wants_to_twist will not be consulted because the player
        # has scored less than 15 points
        new_moves = game_state.calculate_move(deck, player1, lambda:False)
        self.assertEqual(new_moves, [(player1, 2)])
        self.assertItemsEqual(deck, [4])
        self.assertItemsEqual(game_state.moves(), [])

    def test_player_will_stick(self):
        player1 = mock.MagicMock()
        game_state = GameState([(player1, 10), (player1, 8)])
        deck = [2, 4]
        new_moves = game_state.calculate_move(deck, player1, lambda:False)
        self.assertEqual(new_moves, game_state.moves() + [(player1, None)])
        self.assertItemsEqual(deck, [2, 4])
        self.assertItemsEqual(game_state.moves(), [(player1, 10), (player1, 8)])

    def test_player_will_twist(self):
        player1 = mock.MagicMock()
        game_state = GameState([(player1, 10), (player1, 8)])
        deck = [2, 4]
        new_moves = game_state.calculate_move(deck, player1, lambda:True)
        self.assertEqual(new_moves, [(player1, 10), (player1, 8), (player1, 2)])
        self.assertItemsEqual(deck, [4])
        self.assertItemsEqual(game_state.moves(), [(player1, 10), (player1, 8)])

    def test_player_cant_move_if_bust(self):
        player1 = mock.MagicMock()
        game_state = GameState([(player1, 10), (player1, 8), (player1, 10)])
        deck = [ 5 ]
        new_moves = game_state.calculate_move(deck, player1, lambda:True)
        self.assertEqual(new_moves, game_state.moves() + [(player1, None)])
        self.assertEqual(deck,[ 5 ])

    def test_player_cant_move_if_stuck(self):
        player1 = mock.MagicMock()
        player2 = mock.MagicMock()
        game_state = GameState([
            (player1, 10), (player2, 8),
            (player1, 7), (player2, 8),
            (player1, None), (player2, 3),
        ])
        deck = [ 5 ]
        new_moves = game_state.calculate_move(deck, player1, lambda:True)
        self.assertEqual(new_moves, game_state.moves() + [(player1, None)])
        self.assertEqual(deck,[ 5 ])

def calculate_pontoon_winners(game_state):
    sums = game_state.scores()
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

class GameHistory:
    def __init__(self, moves=[]):
        self.__moves = moves

    def moves(self):
        return self.__moves

    def scores(self):
        sums = {}
        for move in self.moves():
            if move[1] is not None:
                sums[move[0]] = sums.get(move[0], 0) + move[1]
        return sums

    def calculate_move(self, deck, player, player_wants_to_twist):
        will_twist = self.player_will_twist(player, player_wants_to_twist)
        card = deck.pop(0) if will_twist else None
        return self.moves()[:] + [(player, card)]

    def player_will_twist(self, player, player_wants_to_twist):
        moves = self.moves()
        score = sum(value for (p, value) in moves
                          if p == player and value is not None)
        player_has_stuck = sum(1 for (p, value) in moves
                                 if p == player and value is None)
        player_must_twist = score < 15
        player_may_twist = not player_has_stuck and score <= 21
        return (player_must_twist
                or (player_may_twist and player_wants_to_twist()))


if __name__ == '__main__':
    unittest.main()
