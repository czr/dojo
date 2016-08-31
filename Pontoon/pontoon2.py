# -*- coding: utf-8 -*-

# TODO:
# - Move calculate_pontoon_winners into GameState
# - Change player mocks to real players or mocks of real players

import mock
import unittest
import random

class GameStateTest(unittest.TestCase):

    def test_one_player(self):
        player = mock.MagicMock()
        game_state = GameState([player], [], [(player, 10), (player, 11)])
        winners = calculate_pontoon_winners(game_state)
        self.assertItemsEqual(winners, [player])

    def test_one_player_stuck(self):
        player = mock.MagicMock()
        game_state = GameState([player], [], [(player, 10), (player, 8), (player, None)])
        winners = calculate_pontoon_winners(game_state)
        self.assertItemsEqual(winners, [player])

    def test_one_player_bust(self):
        player = mock.MagicMock()
        game_state = GameState([player], [], [(player, 10), (player, 11), (player, 2)])
        winners = calculate_pontoon_winners(game_state)
        self.assertItemsEqual(winners, [])

    def test_two_players_second_win(self):
        player1 = mock.MagicMock()
        player2 = mock.MagicMock()
        game_state = GameState([player1, player2], [], [(player1, 10), (player2, 10), (player1, 7), (player2, 8)])
        winners = calculate_pontoon_winners(game_state)
        self.assertItemsEqual(winners, [player2])

    def test_two_players_first_win(self):
        player1 = mock.MagicMock()
        player2 = mock.MagicMock()
        game_state = GameState([player1, player2], [], [(player1, 10), (player2, 10), (player1, 8), (player2, 7)])
        winners = calculate_pontoon_winners(game_state)
        self.assertItemsEqual(winners, [player1])

    def test_two_players_first_passed_bust_second_win(self):
        player1 = mock.MagicMock()
        player2 = mock.MagicMock()
        game_state = GameState([player1, player2], [], [(player1, 10), (player2, 10), (player1, 7), (player2, 8), (player1, 5)])
        winners = calculate_pontoon_winners(game_state)
        self.assertItemsEqual(winners, [player2])

    def test_two_players_with_same_score(self):
        player1 = mock.MagicMock()
        player2 = mock.MagicMock()
        game_state = GameState([player1, player2], [], [(player1, 10), (player2, 10), (player1, 7), (player2, 7)])
        winners = calculate_pontoon_winners(game_state)
        self.assertItemsEqual(winners, [player2, player1])

    def test_three_players_one_winner_one_bust(self):
        player1 = mock.MagicMock()
        player2 = mock.MagicMock()
        player3 = mock.MagicMock()
        game_state = GameState([player1, player2, player3], [], [
            (player1, 10), (player2, 4), (player3, 10),
            (player1, 10), (player2, 5), (player3,  5),
            (player1,  2), (player2, 9)
        ])
        winners = calculate_pontoon_winners(game_state)
        self.assertItemsEqual(winners, [player2])

    def test_player_first_move(self):
        player1 = mock.MagicMock()
        player1.wants_to_twist.return_value = False
        game_state = GameState([player1], [2, 4], [])
        # player_wants_to_twist will not be consulted because the player
        # has scored less than 15 points
        new_game_state = game_state.take_turn()
        self.assertEqual(new_game_state.moves(), [(player1, 2)])
        self.assertEqual(new_game_state.deck(), [4])
        self.assertEqual(game_state.moves(), [])
        self.assertEqual(game_state.deck(), [2, 4])

    def test_player_will_stick(self):
        player1 = mock.MagicMock()
        player1.wants_to_twist.return_value = False
        game_state = GameState([player1], [2, 4], [(player1, 10), (player1, 8)])
        new_game_state = game_state.take_turn()
        self.assertEqual(new_game_state.moves(), game_state.moves() + [(player1, None)])
        self.assertEqual(new_game_state.deck(), [2, 4])
        self.assertEqual(game_state.moves(), [(player1, 10), (player1, 8)])

    def test_player_will_twist(self):
        player1 = mock.MagicMock()
        player1.wants_to_twist.return_value = True
        game_state = GameState([player1], [2, 4], [(player1, 10), (player1, 8)])
        new_game_state = game_state.take_turn()
        self.assertEqual(new_game_state.moves(), [(player1, 10), (player1, 8), (player1, 2)])
        self.assertEqual(new_game_state.deck(), [4])
        self.assertEqual(game_state.moves(), [(player1, 10), (player1, 8)])

    def test_player_cant_move_if_bust(self):
        player1 = mock.MagicMock()
        player1.wants_to_twist.return_value = True
        game_state = GameState([player1], [5], [(player1, 10), (player1, 8), (player1, 10)])
        new_game_state = game_state.take_turn()
        self.assertEqual(new_game_state.moves(), game_state.moves() + [(player1, None)])
        self.assertEqual(new_game_state.deck(), [5])

    def test_player_cant_move_if_stuck(self):
        player1 = mock.MagicMock()
        player1.wants_to_twist.return_value = True
        player2 = Player()
        game_state = GameState([player1, player2], [5], [
            (player1, 10), (player2, 8),
            (player1, 7), (player2, 8),
            (player1, None), (player2, 3),
        ])
        new_game_state = game_state.take_turn()
        self.assertEqual(new_game_state.moves(), game_state.moves() + [(player1, None)])
        self.assertEqual(new_game_state.deck(), [5])

    def test_player2_takes_turn(self):
        player1 = Player()
        player2 = mock.MagicMock(Player)
        player2.wants_to_twist.return_value = True
        game_state = GameState([player1, player2], [5], [
            (player1, 10),
        ])
        new_game_state = game_state.take_turn()
        self.assertEqual(new_game_state.moves(), game_state.moves() + [(player2, 5)])
        self.assertEqual(new_game_state.deck(), [])

    def test_game_finished_one_player_stuck(self):
        player = mock.MagicMock()
        game_state = GameState([player], [], [(player, None)])
        self.assertTrue(game_state.finished())

    def test_game_finished_one_player_no_moves(self):
        player = mock.MagicMock()
        game_state = GameState([player], [], [])
        self.assertFalse(game_state.finished())

    def test_game_finished_two_players_one_stuck(self):
        player1 = mock.MagicMock()
        player2 = mock.MagicMock()
        game_state = GameState([player1, player2], [],
                               [(player1,   10), (player2, 10),
                                (player1,    8), (player2,  2),
                                (player1, None), (player2,  2)])
        self.assertFalse(game_state.finished())

    def test_game_finished_two_players_one_stuck_one_bust(self):
        player1 = mock.MagicMock()
        player2 = mock.MagicMock()
        game_state = GameState([player1, player2], [],
                               [(player1,   10), (player2, 10),
                                (player1,    8), (player2,  2),
                                (player1, None), (player2,  2),
                                (player1, None), (player2, 10)])
        self.assertFalse(game_state.finished())

    def test_game_finished_two_players_one_stuck_one_bust_then_nones(self):
        player1 = mock.MagicMock()
        player2 = mock.MagicMock()
        game_state = GameState([player1, player2], [],
                               [(player1,   10), (player2, 10),
                                (player1,    8), (player2,  2),
                                (player1, None), (player2,  2),
                                (player1, None), (player2, 10),
                                (player1, None), (player2, None)])
        self.assertTrue(game_state.finished())

    def test_game_finished_two_players_one_move(self):
        player1 = mock.MagicMock()
        player2 = mock.MagicMock()
        game_state = GameState([player1, player2], [],
                               [(player1,   10)])
        self.assertFalse(game_state.finished())

    def test_next_player_one_player_no_moves(self):
        player = mock.MagicMock()
        game_state = GameState([player], [], [])
        self.assertEqual(game_state.get_next_player(), player)

    def test_next_player_one_player_one_move(self):
        player = mock.MagicMock()
        game_state = GameState([player], [], [(player, 5)])
        self.assertEqual(game_state.get_next_player(), player)

    def test_next_player_two_players_no_moves(self):
        player1 = mock.MagicMock()
        player2 = mock.MagicMock()
        game_state = GameState([player1, player2], [], [])
        self.assertEqual(game_state.get_next_player(), player1)

    def test_next_player_two_players_one_move(self):
        player1 = mock.MagicMock()
        player2 = mock.MagicMock()
        game_state = GameState([player1, player2], [], [(player1, 5)])
        self.assertEqual(game_state.get_next_player(), player2)

    def test_next_player_two_players_two_moves(self):
        player1 = mock.MagicMock()
        player2 = mock.MagicMock()
        game_state = GameState([player1, player2], [], [(player1, 5), (player2, 5)])
        self.assertEqual(game_state.get_next_player(), player1)



    # def test_game_loop(self):
    #     player1 = mock.MagicMock()
    #     player2 = mock.MagicMock()
    #     game_state = GameState([player1, player2],…)
    #     while not game_state.finished():
    #         game_state = game_state.take_turn(…)

class PlayerTests(unittest.TestCase):
    def test_wants_to_twist(self):
        player = Player()
        self.assertIsInstance(player.wants_to_twist(), bool)

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

class GameState:
    def __init__(self, players, deck, moves):
        self.__players = players
        self.__deck = deck
        self.__moves = moves

    def players(self):
        return self.__players

    def deck(self):
        return self.__deck

    def moves(self):
        return self.__moves

    def scores(self):
        sums = {}
        for move in self.moves():
            if move[1] is not None:
                sums[move[0]] = sums.get(move[0], 0) + move[1]
        return sums

    def finished(self):
        n = len(self.players())
        if len(self.moves()) < n:
            return False
        for player, card in self.moves()[-n:]:
            if card is not None:
                return False
        return True

    def take_turn(self):
        player = self.get_next_player()
        will_twist = self.player_will_twist(player)
        deck = self.deck()[:]
        card = deck.pop(0) if will_twist else None
        return GameState(self.players(), deck, self.moves()[:] + [(player, card)])

    def get_next_player(self):
        if len(self.moves()):
            last_player = self.moves()[-1][0]
        else:
            last_player = self.players()[-1]
        last_player_position = self.players().index(last_player)
        next_player_position = (last_player_position + 1) % len(self.players())
        player = self.players()[next_player_position]
        return player

    def player_will_twist(self, player):
        moves = self.moves()
        score = sum(value for (p, value) in moves
                          if p == player and value is not None)
        player_has_stuck = sum(1 for (p, value) in moves
                                 if p == player and value is None)
        player_must_twist = score < 15
        player_may_twist = not player_has_stuck and score <= 21
        return (player_must_twist
                or (player_may_twist and player.wants_to_twist()))


class Player:
    def wants_to_twist(self):
        return random.choice([True, False])


if __name__ == '__main__':
    unittest.main()
