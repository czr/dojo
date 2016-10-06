import unittest

from word_ladder import word_ladder, mutations
from word_set import WordSet

class WordLadderTest(unittest.TestCase):
    def test_cat_to_cot(self):
        word_set = WordSet(['cat', 'cot'])
        self.assertEqual(word_ladder('cat', 'cot', word_set),
                         ['cat', 'cot'])

    # def test_cat_to_dog(self):
    #     word_set = WordSet(['cat', 'dot', 'cot', 'dog'])
    #     self.assertEqual(word_ladder('cat', 'dog', word_set),
    #                      ['cat', 'cot', 'dot', 'dog'])

    def test_mutations(self):
        alphabet = 'abcd'
        self.assertItemsEqual(mutations('ab', alphabet),
                              ['aa', 'ab', 'ab', 'ac', 'ad', 'bb', 'cb', 'db'])


if __name__ == '__main__':
    unittest.main()
