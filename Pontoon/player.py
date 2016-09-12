import random


class Player:
    def __init__(self, identifier=None):
        self.identifier = identifier


    def __repr__(self):
        return str(self.identifier)


    def wants_to_twist(self):
        return random.choice([True, False])
