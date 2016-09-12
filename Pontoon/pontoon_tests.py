# -*- coding: utf-8 -*-

from game_state import GameState
from player import Player
from game import Game
import mock
import unittest


class GameStateTest(unittest.TestCase):

    def test_one_player(self):
        player = Player()
        game_state = GameState([player], [], [(player, 10), (player, 11)])
        winners = game_state.calculate_winners()
        self.assertItemsEqual(winners, [player])

    def test_one_player_stuck(self):
        player = Player()
        game_state = GameState([player], [], [(player, 10), (player, 8), (player, None)])
        winners = game_state.calculate_winners()
        self.assertItemsEqual(winners, [player])

    def test_one_player_bust(self):
        player = Player()
        game_state = GameState([player], [], [(player, 10), (player, 11), (player, 2)])
        winners = game_state.calculate_winners()
        self.assertItemsEqual(winners, [])

    def test_two_players_second_win(self):
        player1 = Player()
        player2 = Player()
        game_state = GameState([player1, player2], [], [(player1, 10), (player2, 10), (player1, 7), (player2, 8)])
        winners = game_state.calculate_winners()
        self.assertItemsEqual(winners, [player2])

    def test_two_players_first_win(self):
        player1 = Player()
        player2 = Player()
        game_state = GameState([player1, player2], [], [(player1, 10), (player2, 10), (player1, 8), (player2, 7)])
        winners = game_state.calculate_winners()
        self.assertItemsEqual(winners, [player1])

    def test_two_players_first_passed_bust_second_win(self):
        player1 = Player()
        player2 = Player()
        game_state = GameState([player1, player2], [], [(player1, 10), (player2, 10), (player1, 7), (player2, 8), (player1, 5)])
        winners = game_state.calculate_winners()
        self.assertItemsEqual(winners, [player2])

    def test_two_players_with_same_score(self):
        player1 = Player()
        player2 = Player()
        game_state = GameState([player1, player2], [], [(player1, 10), (player2, 10), (player1, 7), (player2, 7)])
        winners = game_state.calculate_winners()
        self.assertItemsEqual(winners, [player2, player1])

    def test_three_players_one_winner_one_bust(self):
        player1 = Player()
        player2 = Player()
        player3 = Player()
        game_state = GameState([player1, player2, player3], [], [
            (player1, 10), (player2, 4), (player3, 10),
            (player1, 10), (player2, 5), (player3,  5),
            (player1,  2), (player2, 9)
        ])
        winners = game_state.calculate_winners()
        self.assertItemsEqual(winners, [player2])

    def test_player_first_move(self):
        player1 = mock.MagicMock(Player)
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
        player1 = mock.MagicMock(Player)
        player1.wants_to_twist.return_value = False
        game_state = GameState([player1], [2, 4], [(player1, 10), (player1, 8)])
        new_game_state = game_state.take_turn()
        self.assertEqual(new_game_state.moves(), game_state.moves() + [(player1, None)])
        self.assertEqual(new_game_state.deck(), [2, 4])
        self.assertEqual(game_state.moves(), [(player1, 10), (player1, 8)])

    def test_player_will_twist(self):
        player1 = mock.MagicMock(Player)
        player1.wants_to_twist.return_value = True
        game_state = GameState([player1], [2, 4], [(player1, 10), (player1, 8)])
        new_game_state = game_state.take_turn()
        self.assertEqual(new_game_state.moves(), [(player1, 10), (player1, 8), (player1, 2)])
        self.assertEqual(new_game_state.deck(), [4])
        self.assertEqual(game_state.moves(), [(player1, 10), (player1, 8)])

    def test_player_cant_move_if_bust(self):
        player1 = mock.MagicMock(Player)
        player1.wants_to_twist.return_value = True
        game_state = GameState([player1], [5], [(player1, 10), (player1, 8), (player1, 10)])
        new_game_state = game_state.take_turn()
        self.assertEqual(new_game_state.moves(), game_state.moves() + [(player1, None)])
        self.assertEqual(new_game_state.deck(), [5])

    def test_player_cant_move_if_stuck(self):
        player1 = mock.MagicMock(Player)
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
        player = Player()
        game_state = GameState([player], [], [(player, None)])
        self.assertTrue(game_state.finished())

    def test_game_finished_one_player_no_moves(self):
        player = Player()
        game_state = GameState([player], [], [])
        self.assertFalse(game_state.finished())

    def test_game_finished_two_players_one_stuck(self):
        player1 = Player()
        player2 = Player()
        game_state = GameState([player1, player2], [],
                               [(player1,   10), (player2, 10),
                                (player1,    8), (player2,  2),
                                (player1, None), (player2,  2)])
        self.assertFalse(game_state.finished())

    def test_game_finished_two_players_one_stuck_one_bust(self):
        player1 = Player()
        player2 = Player()
        game_state = GameState([player1, player2], [],
                               [(player1,   10), (player2, 10),
                                (player1,    8), (player2,  2),
                                (player1, None), (player2,  2),
                                (player1, None), (player2, 10)])
        self.assertFalse(game_state.finished())

    def test_game_finished_two_players_one_stuck_one_bust_then_nones(self):
        player1 = Player()
        player2 = Player()
        game_state = GameState([player1, player2], [],
                               [(player1,   10), (player2, 10),
                                (player1,    8), (player2,  2),
                                (player1, None), (player2,  2),
                                (player1, None), (player2, 10),
                                (player1, None), (player2, None)])
        self.assertTrue(game_state.finished())

    def test_game_finished_two_players_one_move(self):
        player1 = Player()
        player2 = Player()
        game_state = GameState([player1, player2], [],
                               [(player1,   10)])
        self.assertFalse(game_state.finished())

    def test_next_player_one_player_no_moves(self):
        player = Player()
        game_state = GameState([player], [], [])
        self.assertEqual(game_state.get_next_player(), player)

    def test_next_player_one_player_one_move(self):
        player = Player()
        game_state = GameState([player], [], [(player, 5)])
        self.assertEqual(game_state.get_next_player(), player)

    def test_next_player_two_players_no_moves(self):
        player1 = Player()
        player2 = Player()
        game_state = GameState([player1, player2], [], [])
        self.assertEqual(game_state.get_next_player(), player1)

    def test_next_player_two_players_one_move(self):
        player1 = Player()
        player2 = Player()
        game_state = GameState([player1, player2], [], [(player1, 5)])
        self.assertEqual(game_state.get_next_player(), player2)

    def test_next_player_two_players_two_moves(self):
        player1 = Player()
        player2 = Player()
        game_state = GameState([player1, player2], [], [(player1, 5), (player2, 5)])
        self.assertEqual(game_state.get_next_player(), player1)

    def test_generate_deck(self):
        deck = Game.generate_default_deck()
        self.assertEqual(len(deck), 52)
        self.assertEqual(min(deck), 2)
        self.assertEqual(max(deck), 11)
        self.assertEqual(deck.count(2), 4)
        self.assertEqual(deck.count(10), 16)


class GameTests(unittest.TestCase):
    def test_game_loop(self):
        self.assertEqual(Game(2, [11] * 100).play(), [])


class PlayerTests(unittest.TestCase):
    def test_wants_to_twist(self):
        player = Player()
        self.assertIsInstance(player.wants_to_twist(), bool)


if __name__ == '__main__':
    unittest.main()
