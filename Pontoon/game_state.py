class GameState:
    def __init__(self, players, deck, moves):
        self._players = players
        self._deck = deck
        self._moves = moves

    def players(self):
        return self._players

    def deck(self):
        return self._deck

    def moves(self):
        return self._moves

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

    def calculate_winners(self):
        sums = self.scores()
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
