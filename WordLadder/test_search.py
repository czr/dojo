import unittest

from search import search


class SearchTest(unittest.TestCase):

    def test_empty(self):
        self.assertEqual(
            search("", success=lambda path: False, children=lambda path: []),
            None
        )

    def test_found(self):
        def success(path):
            return path == [1, 3, 6]
        prev_pos = 1
        def children(path):
            nonlocal prev_pos
            prev_pos += 2
            return [prev_pos - 1, prev_pos]
        result = search(prev_pos, success=success, children=children)
        self.assertEqual(result, [1, 3, 6])

if __name__ == '__main__':
    unittest.main()
