class WordSet(object):

    def __init__(self, words):
        self.set = {w for w in words}

    def __contains__(self, word):
        return word in self.set

    def filter(self, words):
        return [w for w in words if w in self]
