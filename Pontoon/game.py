from game_state import GameState
from player import Player
import random

class Game(object):

    def __init__(self, num_players, deck=None):
        self.players = [Player() for x in range(num_players)]
        if deck is None:
            deck = self.generate_default_deck()
        self.deck = deck


    def play(self):
        game_state = GameState(self.players, self.deck, [])
        while not game_state.finished():
            game_state = game_state.take_turn()
        return game_state.calculate_winners()


    @staticmethod
    def generate_default_deck():
        numerics = [x for x in range(2,12)] * 4
        pictures = [10] * 12
        deck = numerics + pictures
        random.shuffle(deck)
        return deck

if __name__ == '__main__':
    print Game(4).play()
