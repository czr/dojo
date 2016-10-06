import unittest

from word_set import WordSet

class WordSetTest(unittest.TestCase):

    def test_word_presence(self):
        wordset = WordSet(['cat','dog'])
        self.assertTrue('cat' in wordset)
        self.assertTrue('dog' in wordset)

    def test_word_non_presence(self):
        wordset = WordSet(['cat','dog'])
        self.assertFalse('gerbil' in wordset)

    def test_filter(self):
        word_set = WordSet(['cat', 'dog'])
        self.assertItemsEqual(word_set.filter(['dog','gerbil']),['dog'])


if __name__ == '__main__':
    unittest.main()
