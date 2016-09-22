import unittest

from word_ladder import word_ladder, mutations

class BlahTest(unittest.TestCase):
    def test_cat_to_cot(self):
        wordlist = ['cat', 'cot']
        self.assertEqual(word_ladder('cat', 'cot', wordlist),
                         ['cat', 'cot'])

    # def test_cat_to_dog(self):
    #     wordlist = ['cat', 'DOT', 'cot', 'dog']
    #     self.assertEqual(word_ladder('cat', 'dog', wordlist),
    #                      ['cat', 'cot', 'dot', 'dog'])

    def test_mutations(self):
        alphabet = 'abcd'
        self.assertItemsEqual(mutations('ab', alphabet),
                              ['aa', 'ab', 'ab', 'ac', 'ad', 'bb', 'cb', 'db'])

if __name__ == '__main__':
    unittest.main()
